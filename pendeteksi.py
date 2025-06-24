import sys
import os
import cv2
import time
import threading
import pyttsx3
from ultralytics import YOLO

def resource_path(relative_path):
    # Mendapatkan path ke file resource, baik saat di development atau saat di-build dengan PyInstaller.
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class DrowsinessDetector:
    def __init__(self, eye_threshold=2, mouth_threshold=2):
        # Path ke model yang sudah terintegrasi dalam aplikasi
        default_model_path = resource_path("best.pt")
        self.model = YOLO(default_model_path)

        # Inisialisasi variabel lainnya
        self.cap = cv2.VideoCapture(0)
        self.eye_closed_start_time = None
        self.eye_open_start_time = None
        self.mouth_open_start_time = None
        self.eye_closed_duration = 0
        self.eye_open_duration = 0
        self.mouth_open_duration = 0
        self.eye_threshold = eye_threshold
        self.mouth_threshold = mouth_threshold
        self.is_speaking = False
        self.last_warning_time = 0
        self.warning_cooldown = 5  # Detik

        # Inisialisasi text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')

    def speak_warning(self, message):
        # Play warning messages using text-to-speech.
        if not self.is_speaking:
            self.is_speaking = True
            self.engine.say(message)
            self.engine.runAndWait()
            self.is_speaking = False

    def process_frame(self):
        # Process a single frame for drowsiness detection.
        ret, frame = self.cap.read()
        if not ret:
            return None, "Error: Failed to capture image."

        results = self.model.predict(source=frame, conf=0.7, show=False)
        detections = results[0].boxes

        eye_closed = mouth_open = False
        for box in detections:
            cls_id = int(box.cls)
            confidence = float(box.conf)  # Convert tensor to float
            print(f"Detected class {cls_id} with confidence {confidence:.2f}")  # Debugging log

            if cls_id == 0:  # Eyes closed
                eye_closed = True
            elif cls_id == 1:  # Mouth open
                mouth_open = True

        # Track durations for eyes
        if eye_closed:
            if self.eye_closed_start_time is None:
                self.eye_closed_start_time = time.time()
            self.eye_closed_duration = time.time() - self.eye_closed_start_time
        else:
            self.eye_closed_start_time = None
            self.eye_closed_duration = 0

        if not eye_closed:
            if self.eye_open_start_time is None:
                self.eye_open_start_time = time.time()
            self.eye_open_duration = time.time() - self.eye_open_start_time
        else:
            self.eye_open_start_time = None
            self.eye_open_duration = 0

        # Track durations for mouth
        if mouth_open:
            if self.mouth_open_start_time is None:
                self.mouth_open_start_time = time.time()
            self.mouth_open_duration = time.time() - self.mouth_open_start_time
        else:
            self.mouth_open_start_time = None
            self.mouth_open_duration = 0

        # Check thresholds
        warning_message = None
        current_time = time.time()

        if self.eye_closed_duration > self.eye_threshold and self.eye_open_duration < self.eye_threshold:
            if current_time - self.last_warning_time > self.warning_cooldown:
                warning_message = "Warning: Eyes closed for too long. Please pull over."
                self.last_warning_time = current_time
                self.eye_closed_start_time = None
                self.eye_closed_duration = 0

        elif self.mouth_open_duration > self.mouth_threshold:
            if current_time - self.last_warning_time > self.warning_cooldown:
                warning_message = "You yawn too long, stay focused."
                self.last_warning_time = current_time
                self.mouth_open_start_time = None
                self.mouth_open_duration = 0

        # Speak warning
        if warning_message:
            threading.Thread(target=self.speak_warning, args=(warning_message,)).start()

        # Return annotated frame and any warning
        annotated_frame = results[0].plot()
        return annotated_frame, warning_message

    def release(self):
        """Release resources."""
        self.cap.release()