from flask import Flask, render_template, request, jsonify
import os
from deepface import DeepFace
from speechbrain.inference.speaker import EncoderClassifier
import whisper 

classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper Model
model = whisper.load_model("turbo")

def transcribe_audio(audio_path):
    """Convert speech to text using Whisper."""
    result = model.transcribe(audio_path)
    return result["text"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        name = request.form['name']
        email = request.form['email']
        
        video = request.files['video']
        audio = request.files['audio']
        
        video_path = os.path.join(UPLOAD_FOLDER, f"{name}_{email}_video.webm")
        audio_path = os.path.join(UPLOAD_FOLDER, f"{name}_{email}_audio.webm")
        
        video.save(video_path)
        audio.save(audio_path)

        return jsonify({"message": "Files uploaded successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400

@app.route('/verify', methods=['POST'])
def verify():
    print(request.form)
    name = request.form['name']
    email = request.form['email']
    
    video = request.files['video']
    audio = request.files['audio']

    video_path = os.path.join(UPLOAD_FOLDER, f"{name}_login_video.webm")
    audio_path = os.path.join(UPLOAD_FOLDER, f"{name}_login_audio.webm")

    video.save(video_path)
    audio.save(audio_path)

    stored_video = os.path.join(UPLOAD_FOLDER, f"{name}_{email}_video.webm")
    stored_audio = os.path.join(UPLOAD_FOLDER, f"{name}_{email}_audio.webm")

    try:
        # 1️⃣ Face Matching
        face_match = DeepFace.verify(video_path, stored_video, model_name="Facenet")['verified']

        print(face_match)

        # 2️⃣ Voice Matching
        similarity_score = classifier.verify_files(stored_audio, audio_path)
        voice_match = similarity_score > 0.75  # Set a threshold (0.75 is a good starting point)

        print(voice_match)

        # 3️⃣ Speech-to-Text Matching
        stored_text = transcribe_audio(stored_audio)
        login_text = transcribe_audio(audio_path)
        text_match = stored_text.strip().lower() == login_text.strip().lower()

        if face_match and voice_match and text_match:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "failed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)