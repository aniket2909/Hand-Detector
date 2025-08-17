# ✋ Hand-Detector (MediaPipe Optimized)

This project is a gesture-based automation tool that uses your **webcam** and **hand tracking** to control Google Chrome.  

- Show an **open palm (all 5 fingers visible)** → Chrome **opens**  
- Hide your palm / close your hand → Chrome **closes**  

Originally, this project used a custom `.h5` deep learning model for hand detection.  
In this optimized version, the detection has been replaced with **Google's MediaPipe Hands** solution for **faster, lighter, and more accurate results**.

---

## 🚀 Features

- Real-time hand tracking with **MediaPipe**
- Detects number of visible fingers
- Recognizes a full palm (all 5 fingers extended)
- Cross-platform Chrome open/close support (Windows, macOS, Linux)
- Lightweight (no heavy `.h5` model required)

---

## 📦 Requirements

- Python 3.7+
- OpenCV
- MediaPipe

Install dependencies:
```bash
pip install opencv-python mediapipe
```

---

## ▶️ Usage

Run the script:

```bash
python hand_detector.py
```

- **Show 5 fingers** → Opens Chrome
- **Hide palm / fewer fingers** → Closes Chrome
- Press `q` → Exit the program

---

## 🖥️ How It Works

1. Captures webcam input using OpenCV
2. Uses **MediaPipe Hands** to detect hand landmarks
3. Counts extended fingers:
   - Thumb: checks horizontal position
   - Other fingers: checks vertical position
4. If all 5 fingers are detected → "FULL PALM DETECTED" → Opens Chrome
5. If palm disappears / fewer than 5 fingers → Closes Chrome

---

## ⚡ Optimizations vs Original Project

- Removed dependency on custom `.h5` model
- Integrated **MediaPipe** for better accuracy & speed
- Optimized Chrome detection & launching paths (handles OS-specific edge cases)
- Reduced false triggers with delay throttling

---

## 🖼️ Demo

When you run the script:
- The webcam feed shows hand landmarks
- Finger count displayed on the screen
- Status messages:
  - `"FULL PALM DETECTED - Chrome: OPENING"`
  - `"Show all 5 fingers - Chrome: CLOSING"`

---

## 📌 Notes

- Ensure Chrome is installed in a standard location (script tries common paths)
- Works best in good lighting conditions
- Only supports **1 hand at a time**

---

## 🙌 Credits

- Original project by @aniket2909
- Optimized & refactored with **MediaPipe Hands** by @SH-Nihil-Mukkesh-25
