🔐 AI-Based Multimodal Authentication System
📌 Overview
This project implements a secure, AI-driven authentication system that verifies users using face recognition and voice authentication. It captures video and audio during registration and uses DeepFace for face verification and Wav2Vec2 for voice matching during login.

🚀 Features
✅ Multimodal Authentication: Combines face & voice verification for enhanced security.
✅ Deep Learning Models: Uses DeepFace for face recognition & Wav2Vec2 for voice matching.
✅ Secure & Fast: Efficient real-time authentication process.
✅ Automated Speech Verification: Converts speech to text & validates accuracy.
✅ Flask Backend & Modern UI: Simple, lightweight backend with an interactive UI.

⚙️ Tech Stack
Frontend: HTML, CSS, JavaScript (Media API for recording)

Backend: Flask, OpenCV, DeepFace, Wav2Vec2

Database: (Optional) SQLite / MySQL for storing user metadata

Deployment: Flask Server

📷 How It Works?
1️⃣ Registration:

User enters name and email.

Records video (face) and audio (voice) for 60 seconds.

Data is stored securely.

2️⃣ Login:

User provides name.

Records new video & audio for verification.

Face Matching (DeepFace): Compares the new face with the stored face.

Voice Matching (Wav2Vec2): Converts both audios to text and compares them.

Success → Grants access ✅

Failure → Shows an error ❌
