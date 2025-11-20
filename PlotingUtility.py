import matplotlib.pyplot as plt

class TrajectoryPloter:
    def __init__(self, points):
        self.x1_points = [p[0] for p in points]
        self.x2_points = [p[1] for p in points]
        # Separate x and y coordinates
        x = [p[0] for p in points]
        y = [p[1] for p in points]

        # Plot the trajectory
        fig, ax = plt.subplots()

        ax.plot(x, y, marker='o', linestyle='-', linewidth=1, markersize=2, label='Trajectory')
        #Set limits after plotting
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        ax.set_aspect('equal', 'box')

        plt.figure(figsize=(6, 6))
        plt.gca().set_aspect('equal', 'box')
        plt.autoscale(False)
        """plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.plot(x, y, marker='o', linestyle='-', linewidth=1, markersize=2, label='Trajectory')

        # Optional: improve readability
        plt.title("Trajectory Plot")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.legend()
        plt.axis('equal')  # keep aspect ratio equal"""

        ax.grid(True)
        plt.show()