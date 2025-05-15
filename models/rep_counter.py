import time
from models.exercises import ExerciseConfig


class RepCounter:
    def __init__(self, config: ExerciseConfig):
        self.config = config
        self.state = "start"
        self.reps = 0
        self.last_angle = None
        self.last_time = time.time()
        self.last_rep_time = 0

    def update(self, current_angle):
        current_time = time.time()
        dt = current_time - self.last_time

        # calculate velocity
        velocity = abs(current_angle - self.last_angle) / dt if (self.last_angle and dt > 0) else 0


        # print(f"\nAngle: {current_angle:.1f}° | State: {self.state} | Velocity: {velocity:.1f}°/s")
        # print(f"Thresholds: Flex {self.config.angle_thresholds[0]}°, Extend {self.config.angle_thresholds[1]}°")

        # state machine logic
        if self.state == "extended":
            if (current_angle <= self.config.angle_thresholds[0] and
                    velocity >= self.config.velocity_threshold):
                self.state = "contracted"

                print("→ Transitioned to CONTRACTED")

        elif self.state == "contracted":
            if (current_angle >= self.config.angle_thresholds[1] and
                    (current_time - self.last_rep_time) >= self.config.min_rep_time):
                self.state = "extended"
                self.reps += 1
                self.last_rep_time = current_time
                print(f"→ Transitioned to EXTENDED | Reps: {self.reps}")

        elif self.state == "start":
            if current_angle >= self.config.angle_thresholds[1]:
                self.state = "extended"
                print("→ Initialized to EXTENDED")

        self.last_angle = current_angle
        self.last_time = current_time


        return self.reps