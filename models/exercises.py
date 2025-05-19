from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum
import mediapipe as mp


class BodySide(Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"
    NONE = "none"

class MovementType(Enum):
    EXTENSION = "extension"
    FLEXION = "flexion"
    ROTATION = "rotation"

@dataclass
class ExerciseConfig:
    name: str
    description: str
    target_muscles: List[str]
    body_side: BodySide

    movement_type: MovementType
    angle_thresholds: Tuple[float, float]
    velocity_threshold: float
    min_rep_time: float

    angle_joints: Dict[str, Tuple[int, int, int]]
    ideal_range: Tuple[float, float]

    correct_color: str = "#00FF00"
    incorrect_color: str = "#FF0000"

mp_pose = mp.solutions.pose

# Exercise database
EXERCISES = {
    "bicep_curl": ExerciseConfig(
        name="Bicep Curl",
        description="Flex elbow with controlled motion",
        target_muscles=["biceps brachii", "brachialis"],
        body_side=BodySide.BOTH,
        movement_type=MovementType.FLEXION,
        angle_thresholds=(30, 160),  # 30°=flexed, 160°=extended
        velocity_threshold=20.0,  # 20°/sec minimum
        min_rep_time=0.5,  # 500ms between reps
        angle_joints={
            "left": ( int(mp_pose.PoseLandmark.LEFT_SHOULDER),
                     int(mp_pose.PoseLandmark.LEFT_ELBOW),
                     int(mp_pose.PoseLandmark.LEFT_WRIST)),
            "right": (int(mp_pose.PoseLandmark.RIGHT_SHOULDER),
                      int(mp_pose.PoseLandmark.RIGHT_ELBOW),
                      int(mp_pose.PoseLandmark.RIGHT_WRIST))
        },
        ideal_range=(50, 120)  # Optimal curl range
    ),

    "squat": ExerciseConfig(
        name="Squat",
        description="Lower body until thighs parallel to ground",
        target_muscles=["quadriceps", "glutes"],
        body_side=BodySide.NONE,
        movement_type=MovementType.FLEXION,
        angle_thresholds=(80, 180),  # 80°=flexed, 180°=standing
        velocity_threshold=15.0,
        min_rep_time=1.0,
        angle_joints={
            "main": (int(mp_pose.PoseLandmark.LEFT_HIP),
                     int(mp_pose.PoseLandmark.LEFT_KNEE),
                     int(mp_pose.PoseLandmark.LEFT_ANKLE))
        },
        ideal_range=(90, 140)
    )
}