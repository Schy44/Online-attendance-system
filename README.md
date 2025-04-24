# 📸 Online Attendance System using Python & IoT Camera
An automated, real-time attendance system built with **Python** and an **IoT-based camera** (e.g., Raspberry Pi or ESP32-CAM). The system uses facial recognition to detect and log attendance securely and efficiently, ideal for classrooms, offices, or remote work environments.

---

## 🚀 Features

- 🔍 **Face Detection & Recognition** – Powered by OpenCV and `face_recognition` library
- 📷 **IoT Camera Integration** – Uses low-cost hardware ESP-32 CAM
- 🕒 **Real-Time Attendance Logging** – Auto-records date, time, and identity
- 📊 **Auto-Generated Reports** – Saves attendance logs in CSV/Excel format
- 🌐 **Optional Web Interface** – Built HTML/CSS
- 🔐 **Secure and Local Data Handling**

---

## 🛠️ Tech Stack

- **Languages**: Python 3.x
- **Libraries**: OpenCV, face_recognition, NumPy, pandas
- **Hardware**: ESP32-CAM / USB Webcams
- **Database**: Excel 

---

## 📁 Project Structure

```
attendance-system/
├── camera_module/           # Code to interface with IoT camera
├── face_recognition/        # Scripts for face detection and recognition
├── reports/                 # Generated attendance reports (CSV/Excel)
├── web_interface/           # Optional Flask web app
├── attendance_system.py     # Main attendance recording logic
├── register_faces.py        # Add new faces to the dataset
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/online-attendance-system.git
cd online-attendance-system
```

### 2. Install Dependencies

Make sure Python 3 is installed. Then run:

```bash
pip install -r requirements.txt
```

### 3. Register Faces

Capture and register faces of attendees:

```bash
python register_faces.py
```

### 4. Run the Attendance System

```bash
python attendance_system.py
```

### 5. (Optional) Run the Web Interface

```bash
cd web_interface
python app.py
```

---

## 🧪 Hardware Setup (Example: Raspberry Pi)

1. Connect the Pi Camera or USB Webcam
2. Enable camera support (`sudo raspi-config`)
3. Install Python & dependencies
4. Deploy code from `camera_module` to Pi
5. Use SSH or script automation for remote logging

---

## 📊 Sample Output

- **CSV File:**
```csv
Name,Date,Time
Alice,2025-04-24,09:02:35
Bob,2025-04-24,09:05:17
```

- **Console Log:**
```
[INFO] Detected: Alice at 09:02:35
[INFO] Detected: Bob at 09:05:17
```

---

## 📌 Future Improvements

- Cloud storage for logs
- Multi-angle camera support
- Dashboard with live status and analytics
- Notification system via email/SMS

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for suggestions, bug fixes, or feature requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Your Name**  
[GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile) | [Email](mailto:your.email@example.com)
