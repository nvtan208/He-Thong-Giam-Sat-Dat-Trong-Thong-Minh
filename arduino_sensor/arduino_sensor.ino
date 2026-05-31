#include <SoftwareSerial.h>
#include <DHT.h>

#define DHTPIN      2
#define DHTTYPE     DHT11
#define SOIL_PIN    A0
#define RELAY_PIN   7
#define ESP_RX      8
#define ESP_TX      9
#define ESP_SIGNAL  4

SoftwareSerial espSerial(ESP_RX, ESP_TX);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  espSerial.begin(9600);
  dht.begin();
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(ESP_SIGNAL, INPUT_PULLUP);  // ← Kéo lên nội bộ
  digitalWrite(RELAY_PIN, HIGH);      // Bơm OFF lúc khởi động
  Serial.println("Arduino Ready");
}

void loop() {
  // LOW = bơm BẬT | HIGH = bơm TẮT (INPUT_PULLUP logic)
  bool pumpCmd = !digitalRead(ESP_SIGNAL);
  digitalWrite(RELAY_PIN, pumpCmd ? HIGH : LOW);

  // Đọc sensor
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();
  int   raw  = analogRead(SOIL_PIN);
  int   soil = map(raw, 1023, 0, 0, 100);

  if (isnan(temp)) temp = 0;
  if (isnan(humi)) humi = 0;

  // Gửi sang ESP8266
  espSerial.print(soil);    espSerial.print(",");
  espSerial.print(temp, 1); espSerial.print(",");
  espSerial.println(humi, 1);

  Serial.print("Soil:"); Serial.print(soil);
  Serial.print(" Pump:"); Serial.println(pumpCmd ? "ON" : "OFF");

  delay(2000);
}