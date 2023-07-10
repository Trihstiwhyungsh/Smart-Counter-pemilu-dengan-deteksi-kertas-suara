from app import core, socketio

detection = core.detection.Detection(
    socketio=socketio,
    detect_model="app/core/best2.pt",
    camera_src=0)
