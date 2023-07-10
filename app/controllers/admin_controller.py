import os
import base64
import cv2
import numpy as np
from flask import request, render_template, redirect, url_for
from app import socketio, app, HTTPStatus, services

cookie = os.getenv("CREDENTIALS", default="credentials")
login = services.admin.admin_login_service.login

def base64_to_image(base64_string):
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@socketio.on("connect")
def connect():
    print("Connected")
    socketio.emit("Server Response", {
        "message": "Socket Connected!"
    })

@socketio.on("image")
def gen_frames(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    socketio.emit("processed_image", processed_img_data)

@app.route("/admin")
def admin_page():
    if request.cookies.get(cookie) is None:
        return redirect(url_for("login_page"), code=HTTPStatus.TEMPORARY_REDIRECT)
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        return login(request.form)

    if request.cookies.get(cookie) is None:
        return render_template("auth_page.html")
    return redirect(url_for("admin_page"), code=HTTPStatus.TEMPORARY_REDIRECT)
