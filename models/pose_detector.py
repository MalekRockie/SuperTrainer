import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

class PoseDetector:

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(
            color=(0, 255, 0),
            thickness=2,
            circle_radius=2
        )
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        landmarks = results.pose_landmarks.landmark if results.pose_landmarks else None
        return results, landmarks

    def draw_landmarks(self, frame, results):
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=results.pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec
        )
        return frame

    def get_landmark_indexes(self):
        return {
            'LEFT_SHOULDER': self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            'LEFT_ELBOW': self.mp_pose.PoseLandmark.LEFT_ELBOW,
        }