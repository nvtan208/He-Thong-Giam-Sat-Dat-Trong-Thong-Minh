"""
train_model.py
Chạy script này để retrain model từ data.csv mới
Usage: python train_model.py
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib, json, sys, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
META_PATH  = os.path.join(os.path.dirname(__file__), "model_meta.json")

if not os.path.exists(DATA_PATH):
    print(f"❌ Không tìm thấy {DATA_PATH}")
    print("   Đặt file data.csv vào cùng thư mục với script này")
    sys.exit(1)

print("📂 Đọc data...")
df = pd.read_csv(DATA_PATH)
print(f"   {len(df)} mẫu | Cột: {df.columns.tolist()}")

X = df[['soil', 'temp', 'humidity']]
y = df['watering']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n🌲 Train Decision Tree...")
dt = DecisionTreeClassifier(max_depth=5, random_state=42)
dt.fit(X_train, y_train)
dt_acc = accuracy_score(y_test, dt.predict(X_test))
print(f"   Accuracy: {dt_acc*100:.2f}%")

print("\n🌳 Train Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))
print(f"   Accuracy: {rf_acc*100:.2f}%")

# Chọn model tốt hơn
if rf_acc >= dt_acc:
    best, best_name, best_acc = rf, "RandomForest", rf_acc
else:
    best, best_name, best_acc = dt, "DecisionTree", dt_acc

print(f"\n✅ Chọn: {best_name} ({best_acc*100:.2f}%)")
print(classification_report(y_test, best.predict(X_test),
      target_names=['Không tưới','Tưới']))

fi = best.feature_importances_
print("Feature importance:")
for name, imp in zip(['soil','temp','humidity'], fi):
    bar = '█' * int(imp * 30)
    print(f"  {name:10s} {bar} {imp*100:.1f}%")

# Lưu
joblib.dump(best, MODEL_PATH)
meta = {
    "model_type": best_name,
    "accuracy": round(best_acc * 100, 2),
    "features": ["soil", "temp", "humidity"],
    "classes": ["Không tưới (0)", "Tưới (1)"],
    "feature_importance": {
        "soil":     round(float(fi[0])*100, 1),
        "temp":     round(float(fi[1])*100, 1),
        "humidity": round(float(fi[2])*100, 1)
    },
    "train_samples": len(X_train),
    "test_samples":  len(X_test)
}
with open(META_PATH, 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"\n💾 Đã lưu: model.pkl + model_meta.json")
print("   Restart Flask để áp dụng model mới")
