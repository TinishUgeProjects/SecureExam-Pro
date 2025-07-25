# import cv2
# import pyaudio
# import numpy as np
# import pymongo
# import time
# import threading
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

# class QuizMonitoringSystem(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.start_button = None
#         self.end_button = None
#         self.person_detection_count = 0
#         self.last_save_time = time.time()
#         self.lock = threading.Lock()  # Initialize lock attribute
#         self.is_camera_on = False
#         self.is_microphone_on = False
#         self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
#         self.db = self.mongo_client["quiz_monitoring"]
#         self.collection = self.db["detection_data"]
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Quiz Monitoring System")
#         self.setGeometry(100, 100, 400, 200)
#         self.start_button = QPushButton("Start Exam", self)
#         self.start_button.setGeometry(50, 50, 200, 50)
#         self.start_button.clicked.connect(self.start_exam)
#         self.end_button = QPushButton("End Exam", self)
#         self.end_button.setGeometry(50, 120, 200, 50)
#         self.end_button.clicked.connect(self.end_exam)

#         # Load YOLOv3 model
#         self.net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
#         self.classes = []
#         with open("coco.names", "r") as f:
#             self.classes = [line.strip() for line in f.readlines()]

#     def start_exam(self):
#         self.request_permissions()

#     def request_permissions(self):
#         reply = QMessageBox.question(self, 'Permission Request',
#                                      'Grant access to camera and microphone?',
#                                      QMessageBox.Yes | QMessageBox.No,
#                                      QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             self.handle_permission_granted()
#         else:
#             QMessageBox.information(self, 'Permission Denied',
#                                     'Camera and microphone access denied.')

#     def handle_permission_granted(self):
#         self.start_camera()
#         self.start_microphone()
#         capture_thread = threading.Thread(target=self.capture_and_save_data)
#         capture_thread.start()

#     def start_camera(self):
#         try:
#             self.camera = cv2.VideoCapture(0)
#             self.is_camera_on = True
#         except Exception as e:
#             print("Error starting camera:", e)

#     def start_microphone(self):
#         try:
#             self.microphone = pyaudio.PyAudio()
#             self.stream = self.microphone.open(format=pyaudio.paInt16,
#                                                channels=1,
#                                                rate=44100,
#                                                input=True,
#                                                frames_per_buffer=1024)
#             self.is_microphone_on = True
#         except Exception as e:
#             print("Error starting microphone:", e)

#     def end_exam(self):
#         self.stop_camera()
#         self.stop_microphone()
#         self.exam_terminated = True

#     def stop_camera(self):
#         if self.camera is not None:
#             self.camera.release()
#             self.is_camera_on = False

#     def stop_microphone(self):
#         if self.microphone is not None:
#             self.stream.stop_stream()
#             self.stream.close()
#             self.microphone.terminate()
#             self.is_microphone_on = False

#     def anonymize_data(self, data):
#         data_str = data.tobytes()
#         return hash(data_str)

#     def save_to_database(self, frame_data):
#         current_time = time.time()
#         time_difference = current_time - self.last_save_time

#         if time_difference >= 5:
#             data_to_save = {
#                 "timestamp": current_time,
#                 "frame_data": self.anonymize_data(frame_data),
#                 "person_detection_count": self.person_detection_count
#             }
#             try:
#                 with self.lock:
#                     self.collection.insert_one(data_to_save)
#                     print("Data saved to database:", data_to_save)
#             except Exception as e:
#                 print("Error saving to database:", e)

#             self.last_save_time = current_time

#     def capture_and_save_data(self):
#         last_save_time = time.time()
#         while self.is_camera_on and self.is_microphone_on:
#             ret, frame = self.camera.read()
#             audio_data = self.stream.read(1024)
#             audio_array = np.frombuffer(audio_data, dtype=np.int16)
#             current_time = time.time()
#             time_difference = current_time - last_save_time

#             # Detect persons in the frame
#             self.detect_persons(frame)

#             # Save frame and person detection count to database
#             self.save_to_database(frame)

#             if time_difference >= 5:
#                 # Save to database if 5 seconds have elapsed since the last save
#                 self.save_to_database(frame)
#                 last_save_time = current_time

#             cv2.imshow('Frame', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             time.sleep(0.1)

#         self.stop_camera()
#         self.stop_microphone()
#         cv2.destroyAllWindows()

#     def detect_persons(self, frame):
#         height, width, _ = frame.shape
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         self.net.setInput(blob)
#         outs = self.net.forward(self.net.getUnconnectedOutLayersNames())

#         class_ids = []
#         confidences = []
#         boxes = []

#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5 and class_id == 0:  # Class ID 0 represents a person
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#                     class_ids.append(class_id)
#                     confidences.append(float(confidence))
#                     boxes.append([x, y, w, h])

#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#         persons_detected = len(indexes) if indexes is not None else 0

#         if self.person_detection_count > 0:
#             print(f"Persons detected: {self.person_detection_count}")
#         else:
#             print("No persons detected.")


#         # Update the person_detection_count attribute
#         self.person_detection_count = persons_detected

#     def terminate_exam(self):
#         print("Exam terminated due to unauthorized activity.")
#         self.end_exam()

# if __name__ == "__main__":
#     app = QApplication([])
#     quiz_monitoring_system = QuizMonitoringSystem()
#     quiz_monitoring_system.show()
#     app.exec_()
from flask import Flask, jsonify, request
import cv2
import pyaudio
import numpy as np
import pymongo
import time
import threading

app = Flask(__name__)

class QuizMonitoringSystem:
    def __init__(self):
        self.is_camera_on = False
        self.is_microphone_on = False
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client["quiz_monitoring"]
        self.collection = self.db["detection_data"]
        self.lock = threading.Lock()
        self.net = cv2.dnn.readNet("exam\yolov3.weights", "exam\yolov3.cfg")
        self.classes = []
        with open("exam\coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.start_camera()
        self.start_microphone()
        self.capture_thread = threading.Thread(target=self.capture_and_save_data)
        self.capture_thread.start()

    def start_camera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.is_camera_on = True
        except Exception as e:
            print("Error starting camera:", e)

    def start_microphone(self):
        try:
            self.microphone = pyaudio.PyAudio()
            self.stream = self.microphone.open(format=pyaudio.paInt16,
                                               channels=1,
                                               rate=44100,
                                               input=True,
                                               frames_per_buffer=1024)
            self.is_microphone_on = True
        except Exception as e:
            print("Error starting microphone:", e)

    def stop_camera(self):
        if self.is_camera_on:
            self.camera.release()
            self.is_camera_on = False

    def stop_microphone(self):
        if self.is_microphone_on:
            self.stream.stop_stream()
            self.stream.close()
            self.microphone.terminate()
            self.is_microphone_on = False

    def save_to_database(self, frame_data):
        current_time = time.time()
        data_to_save = {
            "timestamp": current_time,
            "frame_data": self.anonymize_data(frame_data),
            "person_detection_count": self.person_detection_count
        }
        try:
            with self.lock:
                self.collection.insert_one(data_to_save)
        except Exception as e:
            print("Error saving to database:", e)

    def anonymize_data(self, data):
        data_str = data.tobytes()
        return hash(data_str)

    def capture_and_save_data(self):
        last_save_time = time.time()
        while self.is_camera_on and self.is_microphone_on:
            ret, frame = self.camera.read()
            audio_data = self.stream.read(1024)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            current_time = time.time()
            time_difference = current_time - last_save_time

            # Detect persons in the frame
            self.detect_persons(frame)

            # Save frame and person detection count to database
            self.save_to_database(frame)

            if time_difference >= 5:
                # Save to database if 5 seconds have elapsed since the last save
                self.save_to_database(frame)
                last_save_time = current_time

            time.sleep(0.1)  # Sleep to avoid excessive CPU usage

    def detect_persons(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.net.getUnconnectedOutLayersNames())

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # Class ID 0 represents a person
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        persons_detected = len(indexes) if indexes is not None else 0

        return persons_detected

quiz_monitoring_system = None

@app.route('/start-proctoring', methods=['POST'])
def start_proctoring():
    global quiz_monitoring_system
    if quiz_monitoring_system is None:
        quiz_monitoring_system = QuizMonitoringSystem()
        return jsonify({'message': 'Proctoring started'})
    else:
        return jsonify({'message': 'Proctoring already started'})

@app.route('/stop-proctoring', methods=['POST'])
def stop_proctoring():
    global quiz_monitoring_system
    if quiz_monitoring_system is not None:
        quiz_monitoring_system.stop_camera()
        quiz_monitoring_system.stop_microphone()
        quiz_monitoring_system = None
        return jsonify({'message': 'Proctoring stopped'})
    else:
        return jsonify({'message': 'Proctoring not started'})

if __name__ == '__main__':
    app.run(debug=True)
