import matplotlib.pyplot as plt

class TrajectoryPloter:
    def __init__(self, points):
        self.x1_points = [p[0] for p in points]
        self.x2_points = [p[1] for p in points]
        # Separate x and y coordinates
        x = [p[0] for p in points]
        y = [p[1] for p in points]

        # Plot the trajectory
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', linewidth=2, markersize=2, label='Trajectory')

        # Optional: improve readability
        plt.title("Trajectory Plot")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.grid(True)
        plt.legend()
        plt.axis('equal')  # keep aspect ratio equal

        plt.show()