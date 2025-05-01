import time


class RepCounter:
    def __init__(self, contraction_threshold=30, extension_threshold=160, min_rep_time=0.5, min_velocity=20):
        self.contraction_threshold = contraction_threshold
        self.extension_threshold = extension_threshold
        self.reps = 0
        self.state = "extended"
        self.last_rep_time= time.time()
        self.min_rep_time = min_rep_time
        self.min_velocity = min_velocity
        self.last_angle = None
        self.last_time = None

    def update(self, angle):
        current_time = time.time()

        # min time between reps
        if (current_time - self.last_rep_time) < self.min_rep_time:
            return self.reps

        #Velocity checker
        if self.last_angle is not None and self.last_time is not None:
            time_elapsed = current_time - self.last_time
            if time_elapsed == 0:
                return self.reps

            angle_change = abs(angle - self.last_angle)
            velocity = angle_change / time_elapsed

            if velocity < self.min_velocity:
                return self.reps

        if self.state == "extended" and angle < self.contraction_threshold:
                self.state = "contracted"
        elif self.state == "contracted" and angle > self.extension_threshold:
            self.state = "extended"
            self.reps += 1
            self.last_rep_time = current_time
            print(f"Angle: {angle:.1f}° | State: {self.state} | Reps: {self.reps}")
            print("Velocity", velocity)

        self.last_angle = angle
        self.last_time = current_time

        return self.reps