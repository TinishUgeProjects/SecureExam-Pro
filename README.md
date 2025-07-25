# 🎓 SecureExam-Pro: Online Proctoring System with Advanced Data Anonymization

SecureExam-Pro is a privacy-focused online quiz/exam monitoring system built for secure, scalable, and respectful assessments. It ensures academic integrity while protecting user identity using cutting-edge anonymization methods.

## 💡 Features

- ✅ Face detection + real-time face blurring
- ✅ Webcam and screen monitoring
- ✅ Data anonymization techniques to protect user identity
- ✅ Log file generation with anonymized events
- ✅ Compatible with any LMS or quiz portal
- ✅ Lightweight Python-based implementation

## 🧠 Tech Stack

- Python (OpenCV, dlib)
- Tkinter (UI for local deployment)
- Pandas & JSON (for logs & reports)
- Numpy (processing support)

## 🚀 How to Run

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/SecureExam-Pro.git
   cd SecureExam-Pro

2. Install dependencies  
   ```bash
   pip install -r requirements.txt

3. Run the application  
   ```bash
   python app.py

4. Start your quiz/exam in a browser
- The app runs in the background and logs events anonymously.

## 📁 Sample Log Output

{
  "timestamp": "2025-07-25 10:42:13",
  "event": "Face Detected",
  "confidence": 98.2,
  "action": "Blur Applied"
}

## 🔐 Privacy First
- All face data is blurred in real time and never stored. Logs only include anonymized metadata, not identities or raw images.

## 🚧 Future Upgrades
- Role-based admin panel
- Cloud storage for logs
- AI-based behavior detection (suspicious movement, multi-person detection)
