import numpy as np

def calculate_angle(a, b, c):
    """Calculate the angle between 3 points (in 2D)."""
    a = np.array([a.x, a.y])  # First point (e.g., shoulder)
    b = np.array([b.x, b.y])  # Mid point (e.g., elbow)
    c = np.array([c.x, c.y])  # End point (e.g., wrist)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180 / np.pi)
    return angle