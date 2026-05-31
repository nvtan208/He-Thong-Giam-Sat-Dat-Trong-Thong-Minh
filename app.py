from flask import Flask, request, jsonify, render_template
import sqlite3, os, json, joblib, numpy as np
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.json.ensure_ascii = False
DB = "garden.db"

# ── Load AI Model ──
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
META_PATH  = os.path.join(os.path.dirname(__file__), "model_meta.json")

model = joblib.load(MODEL_PATH)
with open(META_PATH) as f:
    model_meta = json.load(f)

print(f"✅ Model loaded: {model_meta['model_type']} — Accuracy {model_meta['accuracy']}%")

# ── Khởi tạo database ──
def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                ts        TEXT NOT NULL,
                soil      INTEGER,
                temp      REAL,
                humidity  REAL,
                pump      INTEGER,
                ai_result TEXT,
                ai_conf   INTEGER
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS pump_log (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                ts     TEXT NOT NULL,
                action TEXT,
                source TEXT
            )
        """)
init_db()

# ── AI Predict dùng model thật ──
def ai_predict(soil, temp, humidity):
    X = pd.DataFrame([[soil, temp, humidity]], columns=['soil', 'temp', 'humidity'])
    pred  = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    conf  = int(round(max(proba) * 100))

    if pred == 1:
        return {
            "decision":   "CAN_TUOI",
            "confidence": conf,
            "reason":     f"Model dự đoán cần tưới (soil={soil}%, conf={conf}%)",
            "label":      "💧 CẦN TƯỚI NƯỚC"
        }
    else:
        return {
            "decision":   "DU_AM",
            "confidence": conf,
            "reason":     f"Model dự đoán đất đủ ẩm (soil={soil}%, conf={conf}%)",
            "label":      "✅ ĐẤT ĐỦ ẨM"
        }

# ── State ──
state = {
    "soil": 0, "temp": 0, "humidity": 0,
    "pump": False, "mode": "auto",
    "last_update": None, "ai": {}
}

# ════════════════════════════════
#  ROUTES - FRONTEND
# ════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html", meta=model_meta)

# ════════════════════════════════
#  ROUTES - ESP8266
# ════════════════════════════════
@app.route("/api/data", methods=["POST"])
def receive_data():
    try:
        d        = request.get_json(force=True)
        soil     = int(d.get("soil", 0))
        temp     = float(d.get("temp", 0))
        humidity = float(d.get("humidity", 0))
        pump     = int(d.get("pump", 0))

        ai = ai_predict(soil, temp, humidity)

        # Auto mode: AI quyết định bơm
        if state["mode"] == "auto":
            state["pump"] = (ai["decision"] == "CAN_TUOI")

        state.update({
            "soil": soil, "temp": temp, "humidity": humidity,
            "last_update": datetime.now().strftime("%H:%M:%S"),
            "ai": ai
        })

        # Lưu DB
        with sqlite3.connect(DB) as con:
            con.execute(
                "INSERT INTO readings (ts,soil,temp,humidity,pump,ai_result,ai_conf) VALUES (?,?,?,?,?,?,?)",
                (datetime.now().isoformat(), soil, temp, humidity,
                 1 if state["pump"] else 0, ai["decision"], ai["confidence"])
            )

        return jsonify({
            "status":   "ok",
            "pump_cmd": 1 if state["pump"] else 0,
            "mode":     state["mode"]
        })

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

# ════════════════════════════════
#  ROUTES - DASHBOARD API
# ════════════════════════════════
@app.route("/api/state")
def get_state():
    return jsonify(state)

@app.route("/api/history")
def get_history():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT ts,soil,temp,humidity,pump,ai_result,ai_conf FROM readings ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/pump", methods=["POST"])
def control_pump():
    d      = request.get_json(force=True)
    action = d.get("action")

    if action == "on":
        state["pump"] = True;  state["mode"] = "manual"
    elif action == "off":
        state["pump"] = False; state["mode"] = "manual"
    elif action == "auto":
        state["mode"] = "auto"
        ai = ai_predict(state["soil"], state["temp"], state["humidity"])
        state["pump"] = (ai["decision"] == "CAN_TUOI")
        state["ai"] = ai

    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT INTO pump_log (ts,action,source) VALUES (?,?,?)",
            (datetime.now().isoformat(), action, "dashboard")
        )

    return jsonify({"status": "ok", "pump": state["pump"], "mode": state["mode"]})

@app.route("/api/model")
def get_model_info():
    return jsonify(model_meta)

if __name__ == "__main__":
    print("\n🌿 Smart Garden — Flask + AI")
    print(f"   Model : {model_meta['model_type']} ({model_meta['accuracy']}% accuracy)")
    print(f"   Data  : {model_meta['train_samples']} mẫu train / {model_meta['test_samples']} mẫu test")
    print( "   URL   : http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
