import cv2
import supervision as sv
from ultralytics import YOLO

# pylint: disable=too-many-arguments
class Detection():
    def __init__(self, socketio, detect_model, camera_src):
        self.socketio = socketio
        self.detect_model = detect_model
        self.camera_src = camera_src
        self.camera = None

    def detect(self, frame):
        model = YOLO(self.detect_model)
        model_frame = model(frame)[0]
        box_anotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )
        detections = sv.Detections.from_yolov8(model_frame)
        labels = [
            f"{model.model.names[class_id]} {confidence: 0.2f}"
            for _, _, confidence, class_id, _ in detections
        ]
        if not labels:
            print("Label kosong mazzeh")
        frame = cv2.flip(frame, 1)
        frame = box_anotator.annotate(scene=frame, detections=detections, labels=labels)
        return frame

    def generate(self):
        if self.camera is None:
            self.open()
        _, frame = self.camera.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        frame = self.detect(frame)
        _, buffer = cv2.imencode(".jpg", frame, encode_param)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def gen_frames(self):
        while True:
            if self.camera is None:
                self.open()
            success, frame = self.camera.read()
            if not success:
                print("Can't read frame from camera!")
                break
            try:
                frame = self.detect(frame)
                if self.camera is None:
                    break
            except Exception as error:
                print(f"[ERROR] {error}")
                self.camera.release()
                self.camera = None
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def open(self):
        self.camera = cv2.VideoCapture(self.camera_src)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

    def close(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            cv2.destroyAllWindows()

    def status(self):
        return self.camera is not None
