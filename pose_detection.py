import sys
import cv2
import mediapipe as mp
from utils.angles import calculate_angle
from rep_counter import RepCounter
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer

# initialize mediaPipe pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# initialze RepCounters
left_counter = RepCounter()
right_counter = RepCounter()

class WorkoutApp(QWidget):
    def __init__(self):
        super().__init__()

        # initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel("Webcam Feed")
        self.video_label.setFixedSize(640, 480)
        self.layout.addWidget(self.video_label)

        # counter texts
        self.left_rep_label = QLabel("Left Reps: 0")
        self.right_rep_label = QLabel("Right Reps: 0")
        self.layout.addWidget(self.left_rep_label)
        self.layout.addWidget(self.right_rep_label)

        # start/stop buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.toggle_webcam)
        self.layout.addWidget(self.start_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.is_running = False

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                background-color: #333;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def toggle_webcam(self):
        if self.is_running:
            self.timer.stop()
            self.start_button.setText("Start")
            self.is_running = False
        else:
            self.timer.start(30)  # Update every 30ms
            self.start_button.setText("Stop")
            self.is_running = True

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

            landmarks = results.pose_landmarks.landmark

            # calculate angles
            left_angle = calculate_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            )
            right_angle = calculate_angle(
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            )

            left_reps = left_counter.update(left_angle)
            right_reps = right_counter.update(right_angle)

            # update the texts
            self.left_rep_label.setText(f"Left Reps: {left_reps}")
            self.right_rep_label.setText(f"Right Reps: {right_reps}")

        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

# run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkoutApp()
    window.setWindowTitle("Workout Tracker")
    window.show()
    sys.exit(app.exec())