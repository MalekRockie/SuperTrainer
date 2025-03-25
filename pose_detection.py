import cv2
import mediapipe as mp
from utils.angles import calculate_angle
from rep_counter import RepCounter

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # For drawing landmarks

cap = cv2.VideoCapture(0)
counter = RepCounter()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert frame to RGB (MediaPipe requires RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Draw landmarks on the frame
    # Inside the loop:
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        angle = calculate_angle(shoulder, elbow, wrist)
        reps = counter.update(angle)
        cv2.putText(frame, f"Reps: {reps}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Pose Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()