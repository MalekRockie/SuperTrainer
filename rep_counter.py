import time


class RepCounter:
    def __init__(self, contraction_threshold=30, extension_threshold=160, min_rep_time=0.5):
        self.contraction_threshold = contraction_threshold
        self.extension_threshold = extension_threshold
        self.reps = 0
        self.state = "extended"
        self.last_rep_time= time.time()
        self.min_rep_time = min_rep_time

    def update(self, angle):
        current_time = time.time()
        if (current_time - self.last_rep_time) < self.min_rep_time:
            return self.reps
        if self.state == "extended" and angle < self.contraction_threshold:
                self.state = "contracted"
        elif self.state == "contracted" and angle > self.extension_threshold:
            self.state = "extended"
            self.reps += 1
            self.last_rep_time = current_time
            print(f"Angle: {angle:.1f}° | State: {self.state} | Reps: {self.reps}")
        return self.reps