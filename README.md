<h1 align="center">HỆ THỐNG GIÁM SÁT CHẤT LƯỢNG ĐẤT TRỒNG THÔNG MINH</h1>

<div align="center">

[![Made with Arduino](https://img.shields.io/badge/Made%20with%20Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![AI Powered](https://img.shields.io/badge/AI%20Powered-Random%20Forest-green?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

<h2 align="center">🌿 Hệ thống giám sát đất trồng thông minh kết hợp AI tự động tưới tiêu</h2>

<p align="center">
Hệ thống sử dụng Arduino Uno R3 thu thập dữ liệu từ cảm biến độ ẩm đất và DHT11, truyền về ESP8266 qua Serial, ESP8266 gửi lên Flask Server qua WiFi. Mô hình AI (Random Forest) được huấn luyện từ 10.000 mẫu dữ liệu thực tế, tự động ra quyết định tưới tiêu với độ chính xác 100%. Toàn bộ hệ thống được giám sát và điều khiển từ xa qua Web Dashboard.
</p>

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

```
Cảm biến đất + DHT11
        ↓
   Arduino Uno R3  ──────── Relay ──── Máy bơm 💧
        ↓ SoftwareSerial (D8/D9)
   ESP8266 NodeMCU ──── GPIO D6 ────► Arduino D4
        ↓ HTTP POST (WiFi)
   Flask Server + AI (Random Forest)
        ↓
   Web Dashboard (localhost:5000)
```

---

## ✨ TÍNH NĂNG

### 🧠 AI Thông minh
- **Mô hình Random Forest** huấn luyện từ 10.000 mẫu dữ liệu thực
- **Độ chính xác 100%** trên 2.000 mẫu test
- **Tự động quyết định** tưới khi độ ẩm đất < 45%
- **Retrain dễ dàng** khi có dữ liệu mới

### 📊 Giám sát thời gian thực
- Hiển thị độ ẩm đất, nhiệt độ, độ ẩm không khí
- Cập nhật mỗi 2 giây
- Lưu lịch sử vào SQLite

### 🎮 Điều khiển linh hoạt
- **Chế độ tự động**: AI quyết định tưới
- **Chế độ thủ công**: Bật/tắt bơm từ web
- Chuyển đổi mượt mà giữa 2 chế độ

---

## 🔧 PHẦN CỨNG SỬ DỤNG

<div align="center">

[![Arduino Uno](https://img.shields.io/badge/Arduino%20Uno%20R3-00979D?style=for-the-badge&logo=arduino&logoColor=white)]()
[![ESP8266](https://img.shields.io/badge/ESP8266%20NodeMCU-blue?style=for-the-badge)]()
[![DHT11](https://img.shields.io/badge/DHT11-green?style=for-the-badge)]()
[![Soil Sensor](https://img.shields.io/badge/Cảm%20biến%20đất-brown?style=for-the-badge)]()
[![Relay](https://img.shields.io/badge/Relay%201%20kênh-purple?style=for-the-badge)]()
[![Pump](https://img.shields.io/badge/Máy%20bơm%205V-blue?style=for-the-badge)]()
[![MB102](https://img.shields.io/badge/MB102%20Power-orange?style=for-the-badge)]()

</div>

---

## 🧮 BẢNG CẮM DÂY

### 🔩 Arduino Uno R3

| Thiết bị | Chân thiết bị | Chân Arduino | Ghi chú |
|---|---|---|---|
| DHT11 | VCC | 5V | Cấp nguồn |
| | GND | GND | |
| | DATA | D2 | + điện trở 10kΩ lên 5V |
| Cảm biến đất | VCC | 5V | Cấp nguồn |
| | GND | GND | |
| | A0 | A0 | Đọc độ ẩm đất |
| | D0 | Không dùng | |
| Relay | S | D7 | Tín hiệu điều khiển |
| | + | 5V MB102 | Nguồn relay |
| | - | GND MB102 | |
| | COM | 5V MB102 | Nguồn cho bơm |
| | NO | Bơm + | Đóng khi relay BẬT |
| | NC | Không dùng | |
| ESP8266 | TX | D8 | SoftwareSerial RX |
| | RX | D9 | SoftwareSerial TX |
| | GND | GND | Chung GND |
| | D6 | D4 | Nhận tín hiệu bơm |
| MB102 | 5V | 5V | Nhận nguồn |
| | GND | GND | |

### 🔩 ESP8266 NodeMCU

| Chân ESP8266 | Nối với | Ghi chú |
|---|---|---|
| TX | D8 Arduino | Gửi data sang Arduino |
| RX | D9 Arduino | Nhận data từ Arduino |
| GND | GND Arduino | Chung GND |
| D6 | D4 Arduino | Tín hiệu điều khiển bơm |
| USB | Củ sạc 5V | Nguồn riêng, không dùng Arduino |

### 🔩 Relay 1 kênh

| Chân Relay | Nối với | Ghi chú |
|---|---|---|
| S | D7 Arduino | Tín hiệu điều khiển |
| + | 5V MB102 | Nguồn |
| - | GND MB102 | |
| COM | 5V MB102 | Nguồn cấp cho bơm |
| NO | Bơm + | Đóng khi relay BẬT |

### 🔩 Máy bơm 5V

| Chân bơm | Nối với | Ghi chú |
|---|---|---|
| + | NO Relay | |
| - | GND MB102 | |

### 🔩 MB102 — Module nguồn

| Chân MB102 | Nối với | Ghi chú |
|---|---|---|
| INPUT | Adapter Jack DC | Nguồn vào |
| 5V | Arduino 5V | Cấp cho Arduino |
| 5V | Relay + | Cấp cho Relay |
| 5V | COM Relay | Nguồn cho bơm |
| GND | Arduino GND | |
| GND | Relay - | |
| GND | Bơm - | |

📌 **Ghi chú quan trọng:**
- ESP8266 dùng **nguồn riêng** (củ sạc USB 5V), không lấy từ Arduino
- DHT11 cần thêm **điện trở 10kΩ** giữa DATA và 5V để đọc đúng
- Arduino và ESP8266 **bắt buộc chung GND**
- Relay loại **Active HIGH**: HIGH = BẬT bơm, LOW = TẮT bơm

---

## 📥 CÀI ĐẶT

### 🛠️ Yêu cầu hệ thống

- 🐍 **Python** `3.8+`
- 📡 **Arduino Uno R3, ESP8266 NodeMCU & Arduino IDE**
- 💾 **RAM** `4GB+`
- 📶 **WiFi** cùng mạng với máy tính chạy Flask

### ⚙️ Thiết lập môi trường

**1. Cài đặt thư viện Python**
```bash
pip install flask scikit-learn joblib numpy pandas
```

**2. Train mô hình AI**
```bash
python train_model.py
```

**3. Cấu hình WiFi trong `esp8266_sender.ino`**
```cpp
const char* WIFI_SSID = "TenWiFi";
const char* WIFI_PASS = "MatKhau";
const char* FLASK_IP  = "192.168.x.x";  // IP máy tính
```
> Tìm IP máy tính: mở CMD → gõ `ipconfig` → tìm IPv4 Address

**4. Nạp code vào phần cứng**
```
Bước 1: Nạp arduino_sensor.ino vào Arduino Uno
Bước 2: Nạp esp8266_sender.ino vào ESP8266
Bước 3: Cắm ESP8266 vào củ sạc 5V (nguồn riêng)
Bước 4: Nối dây theo bảng cắm dây ở trên
```

**5. Chạy Flask Server**
```bash
python app.py
```

**6. Mở Dashboard**
```
http://localhost:5000
```

---

## 🚀 SỬ DỤNG

**Chế độ Tự động:**
- AI tự động phân tích độ ẩm đất mỗi 2 giây
- Khi đất < 45% độ ẩm → tự động bật bơm
- Khi đất đủ ẩm → tự động tắt bơm

**Chế độ Thủ công:**

| Nút | Chức năng |
|---|---|
| 💧 Bật bơm | Bật bơm thủ công |
| ⏹ Tắt bơm | Tắt bơm thủ công |
| ⚡ Tự động | Trả về chế độ AI tự động |

📌 **Ghi chú:** Khi nhấn **Tự động**, hệ thống sẽ quay về chế độ AI, không còn điều khiển thủ công nữa.

---

## 🤖 MÔ HÌNH AI

| Thông số | Giá trị |
|---|---|
| Thuật toán | Random Forest |
| Số cây | 100 |
| Dữ liệu train | 8.000 mẫu |
| Dữ liệu test | 2.000 mẫu |
| Độ chính xác | **100%** |
| Feature quan trọng nhất | Độ ẩm đất (93.1%) |

**Retrain khi có dữ liệu mới:**
```bash
# Đặt file data.csv mới vào thư mục smartgarden/
python train_model.py
# Restart Flask để áp dụng
```

---

## 📁 CẤU TRÚC PROJECT

```
smartgarden/
├── app.py                  ← Flask server + AI prediction
├── train_model.py          ← Script huấn luyện mô hình
├── model.pkl               ← Mô hình Random Forest đã train
├── model_meta.json         ← Thông tin mô hình
├── data.csv                ← Dữ liệu huấn luyện (10.000 mẫu)
├── garden.db               ← SQLite database (tự tạo khi chạy)
├── requirements.txt        ← Thư viện Python
├── templates/
│   └── index.html          ← Web Dashboard
├── arduino_sensor.ino      ← Code Arduino Uno
└── esp8266_sender.ino      ← Code ESP8266
```

---

## 📝 GIẤY PHÉP

© 2025 — Hệ thống Giám sát Chất lượng Đất Trồng Thông minh
