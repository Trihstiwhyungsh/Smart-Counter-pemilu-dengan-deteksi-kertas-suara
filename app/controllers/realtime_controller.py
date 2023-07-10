import base64
from datetime import datetime
from threading import Lock
from random import random, choice
import cv2
import numpy as np
from flask import render_template, request, Response, flash
from app import app, socketio, services

THREAD = None
thread_lock = Lock()
detection = services.detection_service.detection

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread():
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit("updateSensorData", {
            "value": dummy_sensor_value,
            "date": get_current_datetime()
        })
        socketio.sleep(1)

def voting_thread():
    print("Listening election count......")
    paslon = ["P1", "P2", None]
    while True:
        suara = choice(paslon)
        if suara is not None:
            socketio.emit('count', {
                "paslon": suara,
                "suara": "Sah"
            })
            socketio.sleep(1)
        else:
            socketio.emit('count', {
                "paslon": suara,
                "suara": "Tidak Sah"
            })
            socketio.sleep(1)

@app.route('/admin/detection')
def admin():
    camera = request.args.get("camera")
    if camera is not None and camera == "off":
        detection.close()
    if camera is not None and camera == "on":
        detection.open()
        flash("Camera turn on!", "success")
    print("Camera status", detection.status())
    return render_template("detection2.html", is_camera = detection.status())

@app.route("/video")
def video():
    return Response(detection.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin/count')
def index():
    return render_template('landing_page.html')

# @app.route("/admin")
# def admin_index():
#     return render_template('detection.html')

@socketio.on('connect')
def connect():
    global THREAD
    print('Client connected')

    global THREAD
    with thread_lock:
        if THREAD is None:
            THREAD = socketio.start_background_task(voting_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

# ======================================================================++=============
def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

# @socketio.on("image")
# def generate_image(image):
#     detect_image = detection.detect(image)
#     image = base64_to_image(detect_image)
#     frame_resized = cv2.resize(image, (640, 360))
#     encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
#     _, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
#     processed_img_data = base64.b64encode(frame_encoded).decode()
#     processed_img_data = f"data:image/jpg;base64,{processed_img_data}"
#     socketio.emit("processed_image", processed_img_data)
