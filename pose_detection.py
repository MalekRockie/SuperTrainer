import cv2
import mediapipe as mp
from utils.angles import calculate_angle
from rep_counter import RepCounter

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # For drawing landmarks


cap = cv2.VideoCapture(0)
counter = RepCounter()
counter2 = RepCounter()


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert frame to RGB (MediaPipe requires RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Inside the loop:
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        landmarks2 = results.pose_landmarks.landmark
        shoulder2 = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        elbow2 = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        wrist2 = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        angle = calculate_angle(shoulder, elbow, wrist)
        angle2 = calculate_angle(shoulder2, elbow2, wrist2)
        reps = counter.update(angle)
        reps2 = counter2.update(angle2)
        cv2.putText(frame, f"Left Reps: {reps}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Reps: {reps2}", (380, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Pose Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()