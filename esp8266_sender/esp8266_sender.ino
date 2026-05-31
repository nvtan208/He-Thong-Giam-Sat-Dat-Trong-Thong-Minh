#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* WIFI_SSID  = "Huyền Trang T1";
const char* WIFI_PASS  = "huyentrang";
const char* FLASK_IP   = "192.168.1.24";
const int   FLASK_PORT = 5000;

#define PUMP_PIN D6

String inputBuffer = "";
int   soil   = 0;
float temp   = 0;
float humi   = 0;
bool  pumpOn = false;

WiFiClient wifiClient;

void setup() {
  Serial.begin(9600);
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH); // TẮT lúc khởi động
  delay(2000);

  Serial.print("Connecting: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 40) {
    delay(500); Serial.print("."); tries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi OK!");
    Serial.print("IP: "); Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi FAIL!");
  }
}

void loop() {
  // Đọc data từ Arduino
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputBuffer.trim();
      if (inputBuffer.length() > 4) {
        parseData(inputBuffer);
        postToFlask();
      }
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }

  // Poll lệnh bơm mỗi 1 giây
  static unsigned long lastPoll = 0;
  if (millis() - lastPoll > 1000) {
    lastPoll = millis();
    pollPumpCmd();
  }

  yield();
}

void parseData(String data) {
  int c1 = data.indexOf(',');
  int c2 = data.indexOf(',', c1 + 1);
  if (c1 < 0 || c2 < 0) return;
  soil = data.substring(0, c1).toInt();
  temp = data.substring(c1 + 1, c2).toFloat();
  humi = data.substring(c2 + 1).toFloat();
}

void postToFlask() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  String url = "http://" + String(FLASK_IP) + ":" + FLASK_PORT + "/api/data";
  http.begin(wifiClient, url);
  http.addHeader("Content-Type", "application/json");

  String body = "{\"soil\":"     + String(soil)
              + ",\"temp\":"     + String(temp, 1)
              + ",\"humidity\":" + String(humi, 1)
              + ",\"pump\":"     + String(pumpOn ? 1 : 0) + "}";

  int code = http.POST(body);
  if (code == 200) {
    String resp = http.getString();
    int idx = resp.indexOf("pump_cmd\":");
    if (idx >= 0) {
      pumpOn = (resp.charAt(idx + 10) == '1');
      digitalWrite(PUMP_PIN, pumpOn ? LOW : HIGH);
      Serial.println(pumpOn ? "PUMP_ON" : "PUMP_OFF");
    }
  }
  http.end();
}

// Chủ động hỏi Flask mỗi 1 giây
void pollPumpCmd() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  String url = "http://" + String(FLASK_IP) + ":" + FLASK_PORT + "/api/state";
  http.begin(wifiClient, url);
  int code = http.GET();

  if (code == 200) {
    String resp = http.getString();
    bool newPump;
    if (resp.indexOf("\"pump\": true") >= 0 || 
        resp.indexOf("\"pump\":true") >= 0) {
      newPump = true;
    } else {
      newPump = false;
    }

    // Chỉ cập nhật khi trạng thái thay đổi
    if (newPump != pumpOn) {
      pumpOn = newPump;
      digitalWrite(PUMP_PIN, pumpOn ? LOW : HIGH);
      Serial.println(pumpOn ? "PUMP_ON" : "PUMP_OFF");
    }
  }
  http.end();
}