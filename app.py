from flask import Flask, render_template, request, jsonify, Response
import threading
import os
import time
import pyautogui
import cv2
import mediapipe as mp
import joblib
import numpy as np
from werkzeug.utils import secure_filename
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  

ppt_file = ""
is_presentation_running = False
presentation_thread = None

# Load the trained model, scaler, and label encoder
try:
    model = joblib.load("models/gesture_model.pkl")
    scaler = joblib.load("models/gesture_scaler.pkl")
    label_encoder = joblib.load("models/gesture_label_encoder.pkl")
    logger.info("Successfully loaded ML models")
except Exception as e:
    logger.error(f"Error loading ML models: {str(e)}")
    raise

# Real-time gesture recognition loop
def gesture_loop():
    global is_presentation_running
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    cap = cv2.VideoCapture(0)

    gesture_history = []
    max_history = 10
    last_action_time = 0
    cooldown = 1.5  # seconds

    while is_presentation_running:
        success, frame = cap.read()
        if not success:
            logger.error("Failed to read from camera")
            break
        frame = cv2.flip(frame, 1)
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if result.multi_hand_landmarks:
            landmarks = []
            for lm in result.multi_hand_landmarks[0].landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            try:
                X = scaler.transform([landmarks])
                pred = model.predict(X)
                label = label_encoder.inverse_transform(pred)[0]

                gesture_history.append(label)
                if len(gesture_history) > max_history:
                    gesture_history.pop(0)

                most_common = max(set(gesture_history), key=gesture_history.count)
                if gesture_history.count(most_common) >= 3 and time.time() - last_action_time > cooldown:
                    logger.info(f"Gesture triggered: {most_common}")
                    if most_common == "swipe_right":
                        pyautogui.press("right")
                    elif most_common == "swipe_left":
                        pyautogui.press("left")
                    elif most_common == "zoom_in":
                        pyautogui.hotkey("ctrl", "+")
                    elif most_common == "point":
                        screen_width, screen_height = pyautogui.size()
                        pyautogui.moveTo(screen_width // 2, screen_height // 2)

                    gesture_history.clear()
                    last_action_time = time.time()

            except Exception as e:
                logger.error(f"Prediction error: {e}")

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=["POST"])
def upload():
    global ppt_file, is_presentation_running, presentation_thread
    logger.info("Received upload request")

    if is_presentation_running:
        return jsonify({"status": "error", "message": "A presentation is already running"}), 400

    if 'ppt' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400

    file = request.files['ppt']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if not file.filename.endswith(('.ppt', '.pptx')):
        return jsonify({"status": "error", "message": "Invalid file type. Please upload a PowerPoint file"}), 400

    try:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        filename = secure_filename(file.filename)
        ppt_file = os.path.join(upload_dir, filename)
        file.save(ppt_file)

        if not os.path.exists(ppt_file):
            raise Exception("File was not saved successfully")

        is_presentation_running = True
        presentation_thread = threading.Thread(target=launch_and_control, daemon=True)
        presentation_thread.start()

        logger.info("Presentation started successfully")
        return jsonify({
            "status": "success",
            "message": "Presentation started successfully",
            "filename": filename
        }), 200

    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def launch_and_control():
    global ppt_file, is_presentation_running
    try:
        logger.info(f"Launching presentation: {ppt_file}")
        os.startfile(ppt_file)
        time.sleep(2)
        pyautogui.press("f5")
        gesture_loop()
    except Exception as e:
        logger.error(f"Error in presentation control: {str(e)}")
    finally:
        is_presentation_running = False
        logger.info("Presentation ended")


@app.route('/stop', methods=["POST"])
def stop():
    global is_presentation_running
    is_presentation_running = False
    return jsonify({"status": "success", "message": "Presentation stopped"})


@app.route('/status')
def get_status():
    return jsonify({"is_running": is_presentation_running})


def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
