import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_trajectory(trajectories, traj_colors, Regions):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))

    # Define regions as rectangles [x, y, width, height]
    # Green region (bottom left)

    rectangles = []
    for region in Regions:
        width = region[1][0] - region[0][0]
        height = region[1][1] - region[0][1]

        rectangles.append(patches.Rectangle(region[0], width, height,
                                   linewidth=1, edgecolor=Regions[region][0],
                                   facecolor=Regions[region][1], alpha=0.5))

    # Add rectangles to plot
    for rect in rectangles:
        ax.add_patch(rect)

    # Plot the trajectory
    for i, points in enumerate(trajectories):
        x = [p[0] for p in points]
        y = [p[1] for p in points]

        ax.plot(
            x, y,
            marker='o', markerfacecolor='none',
            linestyle='-', linewidth=0.5,
            markersize=2.5,
            color=traj_colors[i % len(traj_colors)],
            label=f'Trajectory {i + 1}',
            zorder=5
        )

    # Set limits and aspect
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal', 'box')

    # Labels and title
    ax.set_xlabel('x₁', fontsize=12)
    ax.set_ylabel('x₂', fontsize=12)
    ax.set_title('Trajectory Plot with Regions', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()