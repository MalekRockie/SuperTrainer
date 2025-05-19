import sys
from PySide6.QtWidgets import QApplication
from controllers.workout_controller import WorkoutController
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)


    controller = WorkoutController()
    window = MainWindow(controller)

    controller.connect_to_window(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()