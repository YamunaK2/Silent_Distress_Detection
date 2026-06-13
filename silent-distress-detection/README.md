# Silent Distress Detection AI

A privacy-first, edge-AI system to detect silent distress signals (micro-expressions, posture, audio) and alert personnel via a real-time dashboard.

## 🚀 Features

- **Multimodal AI**: Combines Facial Micro-expressions (OpenCV), Posture Analysis (Motion/Shape), and Audio Stress (Simulation).
- **Privacy First**: No video recording. No face recognition/identity storage. Only temporal alert metadata is saved.
- **Real-Time Dashboard**: React-based UI to monitor system status and view alerts.
- **Human-in-the-Loop**: Alerts require human confirmation to minimize false positives.
- **Edge Processing**: All AI processing runs locally on the backend.

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, OpenCV, NumPy, TensorFlow
- **Frontend**: React (Create React App), CSS3
- **Database/Notification**: Google Firebase (Firestore, Cloud Messaging)

## 📂 Project Structure

```
silent-distress-detection/
├── backend/            # Python FastAPI Server + AI Logic
│   ├── ai/             # Computer Vision & Audio Modules
│   ├── alerts/         # Alert Logic & Firebase Connector
│   └── app.py          # Main Entry Point
├── frontend/           # React Web Application
│   ├── src/pages/      # Dashboard, Alerts, Settings
│   └── src/services/   # API & Firebase Services
└── firebase/           # Firestore Rules
```

## ⚡ Quick Start

### 1. Backend Setup

1. Navigate to backend: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate venv:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python app.py` (or `uvicorn app:app --reload`)

**Note on Firebase**: By default, the system runs in **Mock Mode** (alerts stored in memory) if no `serviceAccountKey.json` is found. To connect real Firebase:
- Place your `serviceAccountKey.json` on your machine.
- Set `GOOGLE_APPLICATION_CREDENTIALS` env var to point to it.

### 2. Frontend Setup

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. Open browser at `http://localhost:5173`

## 🛡 Privacy & Ethics

- **No Surveillance**: This is NOT a surveillance system. It does not record video.
- **No Identity**: It detects *emotions* and *distress*, not *people*. It cannot tell "Who" is in distress, only "That" someone is.
- **Ephemeral Processing**: Video frames are processed in RAM and discarded immediately.

## 📸 Usage

1. Go to the **Dashboard** page.
2. Click **Start Monitoring**.
3. If using a webcam, simulate distress (e.g., frowning, hands up, freezing).
4. Watch the **Alerts** page for incoming notifications.
5. **Confirm** or **Dismiss** alerts to train the system logic (mock).

---
*Created for AI Safety Hackathon*
