# 🏋️ AI Real-Time Gym Coach

An intelligent fitness assistant that uses AI-powered pose detection and computer vision to analyze workouts in real time. The system detects body posture, counts repetitions, tracks sets, and provides instant voice coaching through a live webcam interface.

---

## 🚀 Features

- **Real-Time Pose Detection** — Uses MediaPipe to track 33 body landmarks via webcam
- **5 Exercise Support** — Squats, Push-ups, Bicep Curls, Shoulder Press, Lunges
- **Automatic Rep & Set Counting** — Tracks reps by analyzing joint angles in real time
- **AI Voice Coaching** — Groq LLM generates personalized feedback, delivered via gTTS text-to-speech
- **Live Pose Overlay** — Skeleton visualization drawn on webcam feed using OpenCV
- **Exercise Form Feedback** — Detects depth, alignment, swing, and balance issues
- **User Authentication** — Simple login system with per-user data isolation
- **Workout History** — Tracks reps, sets, and duration per session in SQLite database

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web application framework |
| MediaPipe | Pose landmark detection |
| OpenCV | Video processing and skeleton drawing |
| Streamlit-WebRTC | Live webcam streaming |
| Groq LLM | AI voice coaching generation |
| gTTS | Text-to-speech audio output |
| SQLite | Workout history database |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```
AI-GYM-Trainer/
│
├── main.py                          # Main Streamlit app
├── requirements.txt                 # Python dependencies
├── packages.txt                     # System dependencies
├── Dockerfile                       # Docker configuration
├── data.db                          # SQLite database (auto-created)
│
├── static/
│   └── style.css                    # Custom CSS styles
│
├── ml_models/
│   └── pose_landmarker_full.task    # MediaPipe pose model
│
├── detectors/
│   ├── squat.py                     # Squat detection logic
│   ├── pushup.py                    # Push-up detection logic
│   ├── biceps_curl.py               # Bicep curl detection logic
│   ├── shoulder_press.py            # Shoulder press detection logic
│   └── lunges.py                    # Lunges detection logic
│
└── services/
    ├── auth/                        # Login and authentication
    ├── coaching/                    # LLM + TTS voice pipeline
    ├── config/                      # Exercise configuration
    ├── persistence/                 # Database repository
    ├── state/                       # Session state management
    ├── tracking/                    # Metrics sync
    ├── ui/                          # Style loader
    └── vision/                      # WebRTC video processor
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Himanshusinghyadavup61/Realtime-AI-GYM-Trainer.git
cd Realtime-AI-GYM-Trainer
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com

### 5. Run the app

```bash
streamlit run main.py
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLM voice coaching | ✅ Yes |

---

## 📊 Supported Exercises

| Exercise | Metrics Tracked |
|---|---|
| Squats | Knee angle, back angle, depth status |
| Push-ups | Elbow angle, body alignment, hip position |
| Bicep Curls | Elbow angle, shoulder stability, swing detection |
| Shoulder Press | Elbow angle, arm extension, back arch |
| Lunges | Front knee angle, torso angle, balance status |

---

## 🗄️ Database

The app uses SQLite to store workout history with IST timezone handling:

- **Users table** — Stores usernames with creation timestamps
- **Exercises table** — Logs exercise name, reps, sets, duration, and date per session
- Same exercise on the same day is updated (not duplicated)

---

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Add `GROQ_API_KEY` in Secrets
5. Deploy

### Docker

```bash
docker build -t ai-gym-trainer .
docker run -p 7860:7860 ai-gym-trainer
```

---

## 📝 Requirements

```
streamlit>=1.40.0
streamlit-webrtc==0.47.1
tornado==6.2
numpy==1.26.4
mediapipe==0.10.35
opencv-python-headless==4.8.0.76
pandas==2.2.3
groq>=0.12.0
gtts==2.5.3
python-dotenv==1.2.2
```

---

## 👤 Author

**Himanshu Singh Yadav**
- GitHub: [@Himanshusinghyadavup61](https://github.com/Himanshusinghyadavup61)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
