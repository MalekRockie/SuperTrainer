class RepCounter:
    def __init__(self, threshold=30):
        self.threshold = threshold
        self.reps = 0
        self.is_contracted = False

    def update(self, angle):
        if angle < self.threshold and not self.is_contracted:
            self.reps += 1
            self.is_contracted = True
        elif angle > 160 and self.is_contracted:
            self.is_contracted = False
        return self.reps