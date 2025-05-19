from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from models.exercises import EXERCISES


class MainWindow(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        self.setup_style()
        self.setup_connections()

        self.left_rep_label = QLabel("Left Reps: 0")
        self.right_rep_label = QLabel("Right Reps: 0")
        self.layout.addWidget(self.left_rep_label)
        self.layout.addWidget(self.right_rep_label)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel("Video Feed")
        self.video_label.setFixedSize(640, 480)
        self.layout.addWidget(self.video_label)

        self.exercise_dropdown = QComboBox()
        self.exercise_dropdown.addItems(EXERCISES.keys())
        self.layout.addWidget(self.exercise_dropdown)

        self.start_exercise_btn = QPushButton("Start Exercise")
        self.start_exercise_btn.clicked.connect(self.start_exercise)
        self.layout.addWidget(self.start_exercise_btn)

    def setup_connections(self):
        self.start_exercise_btn.clicked.connect(self.start_exercise)
        print("Connection initialized")

    def setup_style(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                background-color: #333;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton{
                font-size: 16px;
                background-color: #4CAF50
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049
            }
        """)

    def update_frame(self, frame):
        try:
            h, w, ch = frame.shape
            bytes_per_line = ch * w

            if ch == 3:
                qt_format = QImage.Format_RGB888
            elif ch == 4:
                qt_format = QImage.Format_RGBA8888
            else:
                raise ValueError(f"Unexpected number of channels: {ch}")

            qt_image = QImage(frame.data, w, h, bytes_per_line, qt_format)

            if qt_image.isNull():
                print("Error: Failed to create QImage from frame")
                return

            self.video_label.setPixmap(QPixmap.fromImage(qt_image))


        except Exception as e:
            print(f"Frame update error: {str(e)}")

    def start_exercise(self):
        print("started")
        exercise = self.exercise_dropdown.currentText()
        # print(f"selected exercise: {exercise}")

        try:
            self.controller.set_exercise(exercise)
            if self.controller.start_processing():
                print("Processing started successfully")
            else:
                print("Processing was already running")
        except Exception as e:
            print(f"Error starting exercise: {str(e)}")
            self.show_error_message(str(e))

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText("Error")
        error_box.setInformativeText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

    def update_reps(self, reps):
        # self.rep_label.setText(f"Reps: {reps}")
        if "left" in reps and "right" in reps:
            self.left_rep_label.setText(f"Left Reps: {reps['left']}")
            self.right_rep_label.setText(f"Right Reps: {reps['right']}")
            self.right_rep_label.show()
