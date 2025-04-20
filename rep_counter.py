class RepCounter:
    def __init__(self, contraction_threshold=30, extension_threshold=160):
        self.contraction_threshold = contraction_threshold
        self.extension_threshold = extension_threshold
        self.reps = 0
        self.state = "extended"

    def update(self, angle):
        if self.state == "extended":
            if angle < self.contraction_threshold:
                self.state = "contracted"
        elif self.state == "contracted":
            if angle > self.extension_threshold:
                self.state = "extended"
                self.reps += 1
                print("count", self.reps)
        return self.reps