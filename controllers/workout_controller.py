from PySide6.QtCore import QTimer
import cv2
import mediapipe as mp
from models.exercises import EXERCISES, BodySide
from models.rep_counter import RepCounter
from utils.angles import calculate_angle


class WorkoutController:
    def __init__(self):
        self.timer = QTimer()
        self.is_processing = False


        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error could not open camera")
            for i in range(3):
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    print(f"opened camera at index {i}")
                    break
                else:
                    raise RuntimeError("Could not open any video device")
            ret, test_frame = self.cap.read()
            if not ret:
                print("Warning could not read test frame from camera")
        self.mp_pose = mp.solutions.pose
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.current_exercise = None
        self.counters = {}
        self.frame_count = 0

        print(f"Webcam opened: {self.cap.isOpened()}")


    def start_processing(self):
        if not self.is_processing:
            print("Should start the processing......")
            print(f"Timer is connected: {self.timer.isActive()}")
            print(f"camera is open: {self.cap.isOpened()}")
            print(f"current exercise: {self.current_exercise.name if self.current_exercise else None}")
            self.timer.start(30)  # ~30 FPS
            self.is_processing = True
            return True
        return False

    def stop_processing(self):
        if self.is_processing:
            print("should stop....")
            self.timer.stop()
            self.is_processing = False
            return True
        return False

    def connect_to_window(self, window):
        self.timer.timeout.connect(self.process_frame)
        self.on_frame_processed = window.update_frame
        self.on_reps_updated = window.update_reps
        print(f"Timer connected: {self.timer.isActive()}")

    def process_frame(self):

        if not self.current_exercise:
            return


        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return

        # Convert to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False  # Improves performance

        # Convert back to BGR for OpenCV drawing
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        # Process with MediaPipe
        results = self.pose.process(frame_rgb)

        reps = {}

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
                )
            # reps = self.on_reps_updated()
            # print(reps)

        else:
            landmark = None
            # print("No pose landmark detected in this frame")

        if self.current_exercise.body_side == BodySide.BOTH:
            for side in ["left", "right"]:
                a,b,c = self.current_exercise.angle_joints[side]
                angle = calculate_angle(landmarks[a],
                                        landmarks[b],
                                        landmarks[c])
                # print(f"{side} angle: {angle}°")
                reps[side] = self.counters[side].update(angle)
                self.on_reps_updated(reps)
                # print(f"reps: {reps[side]}")
        else:
            a,b,c = self.current_exercise.angle_joints["main"]
            angle = calculate_angle(
                landmarks[a],
                landmarks[b],
                landmarks[c]
            )

            self.on_reps_updated(reps)
            reps["main"] = self.counters["main"].update(angle)



        # Convert back to RGB for Qt display
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.on_frame_processed(display_frame)

    def _process_landmarks(self, landmarks):
        if not landmarks or not self.current_exercise:
            return {"left": 0, "right": 0}

        try:
            reps = {"left": 0, "right": 0}

            if self.current_exercise.body_side == BodySide.BOTH:
                # process left side
                l_shoulder, l_elbow, l_wrist = self.current_exercise.keypoints["left"]
                left_angle = calculate_angle(
                    landmarks[l_shoulder],
                    landmarks[l_elbow],
                    landmarks[l_wrist]
                )
                reps["left"] = self.counters["left"].update(left_angle)

                # process right side
                r_shoulder, r_elbow, r_wrist = self.current_exercise.keypoints["right"]
                right_angle = calculate_angle(
                    landmarks[r_shoulder],
                    landmarks[r_elbow],
                    landmarks[r_wrist]
                )
                reps["right"] = self.counters["right"].update(right_angle)

            else:  # one side exercise
                kp1, kp2, kp3 = self.current_exercise.keypoints["main"]
                angle = calculate_angle(
                    landmarks[kp1],
                    landmarks[kp2],
                    landmarks[kp3]
                )
                reps["main"] = self.counters["main"].update(angle)

            return reps

        except Exception as e:
            print(f"Landmark processing error: {str(e)}")
            return {"left": 0, "right": 0}

    def set_exercise(self, exercise_name):
        print(f"Setting exercise: {exercise_name}")
        if exercise_name not in EXERCISES:
            raise ValueError(f"Uknown exercise: {exercise_name}")
        self.current_exercise = EXERCISES[exercise_name]
        self._setup_counters()
        print(f"Exercise set: {self.current_exercise.name}")

    def _setup_counters(self):
        self.counters = {}
        if self.current_exercise.body_side == BodySide.BOTH:
            self.counters["left"] = RepCounter(self.current_exercise)
            self.counters["right"] = RepCounter(self.current_exercise)

        else:
            self.counters["main"] = RepCounter(self.current_exercise)

    def __del__(self):
        self.cap.release()