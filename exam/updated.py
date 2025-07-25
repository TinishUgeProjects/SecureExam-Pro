import cv2
import pyaudio
import numpy as np
import pymongo
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox


class QuizMonitoringSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.microphone = None
        self.stream = None
        self.is_camera_on = False
        self.is_microphone_on = False
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.mongo_client["quiz_monitoring"]
        self.collection = self.db["proctoring_data"]
        self.lock = threading.Lock()

        self.setWindowTitle("Quiz Monitoring System")
        self.setGeometry(100, 100, 400, 200)

        self.permission_button = QPushButton("Request Permissions", self)
        self.permission_button.setGeometry(50, 50, 200, 50)
        self.permission_button.clicked.connect(self.request_permissions)
        self.last_save_time = time.time()

    def request_permissions(self):
        # Display a QMessageBox to prompt the user for permissions
        reply = QMessageBox.question(self, 'Permission Request',
                                     'Grant access to camera and microphone?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Permissions granted, proceed with starting camera and microphone
            self.handle_permission_granted()
        else:
            # Permissions denied, handle accordingly (e.g., display message)
            self.handle_permission_denied()

    def handle_permission_denied(self):
        # Handle case where permissions are denied
        QMessageBox.information(self, 'Permission Denied',
                                'Camera and microphone access denied.')

    def handle_permission_granted(self):
        # Start camera and microphone
        self.start_camera()
        self.start_microphone()

        # Start capturing and saving data
        capture_thread = threading.Thread(target=self.capture_and_save_data)
        capture_thread.start()
        capture_thread.join()

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
        if self.camera is not None:
            self.camera.release()
            self.is_camera_on = False

    def stop_microphone(self):
        if self.microphone is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.microphone.terminate()
            self.is_microphone_on = False

    def anonymize_data(self, data):
        # Convert numpy array to a hashable data type (e.g., string)
        data_str = data.tostring()
        # Hash the string representation
        return hash(data_str)

    def save_to_database(self, video_data, audio_data):
        current_time = time.time()
        data_to_save = {
            "timestamp": current_time,
            "video_data": cv2.imencode('.jpg', video_data)[1].tobytes(),
            "audio_data": audio_data.tobytes()
        }
        try:
            with self.lock:
                self.collection.insert_one(data_to_save)
        except Exception as e:
            print("Error saving to database:", e)

    def capture_and_save_data(self):
        last_save_time = time.time()  # Initialize the last save time
        while self.is_camera_on and self.is_microphone_on:
            # Capture frame from camera
            ret, frame = self.camera.read()

            # Capture audio from microphone
            audio_data = self.stream.read(1024)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Calculate the time difference since the last save
            current_time = time.time()
            time_difference = current_time - last_save_time

            # Save to database if 5 seconds have elapsed since the last save
            if time_difference >= 5:
                self.save_to_database(frame, audio_array)
                last_save_time = current_time  # Update the last save time

            # Display frame (optional)
            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            time.sleep(0.1)  # Sleep for a short duration to avoid high CPU usage

        # Release resources
        self.stop_camera()
        self.stop_microphone()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication([])
    quiz_monitoring_system = QuizMonitoringSystem()
    quiz_monitoring_system.show()
    app.exec_()
