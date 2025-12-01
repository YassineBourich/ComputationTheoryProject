import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def plot_trajectory(trajectories, traj_colors, Regions):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Determine if we're dealing with 2D or 3D regions/trajectories
    # Check first region to determine dimensionality
    first_region = next(iter(Regions.keys()))
    is_3d = len(first_region[0]) == 3

    # Plot regions as rectangles
    rectangles = []
    for region in Regions:
        # Extract 2D coordinates (x, y) - ignore z/theta for 3D cases
        if is_3d:
            x_min, y_min = region[0][0], region[0][1]
            x_max, y_max = region[1][0], region[1][1]
        else:
            x_min, y_min = region[0][0], region[0][1]
            x_max, y_max = region[1][0], region[1][1]
        
        width = x_max - x_min
        height = y_max - y_min

        rectangles.append(patches.Rectangle(
            (x_min, y_min), width, height,
            linewidth=2, edgecolor=Regions[region][0],
            facecolor=Regions[region][1], alpha=0.4,
            zorder=1
        ))

    # Add rectangles to plot
    for rect in rectangles:
        ax.add_patch(rect)

    # Plot trajectories with arrows to show direction
    for i, points in enumerate(trajectories):
        if not points:
            print(f"Warning: Trajectory {i+1} is empty, skipping.")
            continue
        
        # Ensure points are lists/arrays of numbers, not tuples of tuples
        # Extract 2D coordinates (x, y) - ignore z/theta for 3D cases
        try:
            x = [float(p[0]) for p in points]
            y = [float(p[1]) for p in points]
        except (TypeError, IndexError) as e:
            print(f"Error extracting coordinates from trajectory {i+1}: {e}")
            print(f"First point: {points[0] if points else 'N/A'}")
            continue

        color = traj_colors[i % len(traj_colors)]
        
        # Plot start and end points with special markers
        if len(x) > 0:
            ax.plot(x[0], y[0], marker='s', markersize=8, color=color, 
                   markeredgecolor='black', markeredgewidth=1.5, 
                   zorder=7, label='Start' if i == 0 else '')
            if len(x) > 1:
                ax.plot(x[-1], y[-1], marker='*', markersize=12, color=color,
                       markeredgecolor='black', markeredgewidth=1.5,
                       zorder=7, label='End' if i == 0 else '')
        
        # Plot the trajectory line
        ax.plot(
            x, y,
            marker='o', markerfacecolor='none',
            linestyle='-', linewidth=1.5,
            markersize=3,
            color=color,
            zorder=5,
            label=f'Trajectory {i+1}' if len(trajectories) > 1 else 'Trajectory'
        )
        
        # Add arrows to show direction (every Nth point to avoid clutter)
        if len(x) > 1:
            # Show arrows for about 15-20 points along the trajectory
            step = max(1, len(x) // 20)
            arrow_indices = list(range(0, len(x)-1, step))
            for idx in arrow_indices:
                if idx < len(x) - 1:
                    dx = x[idx+1] - x[idx]
                    dy = y[idx+1] - y[idx]
                    # Normalize arrow length
                    length = np.sqrt(dx**2 + dy**2)
                    if length > 0.01:  # Only draw arrows for meaningful movement
                        dx = dx / length * 0.3
                        dy = dy / length * 0.3
                        ax.arrow(x[idx], y[idx], dx, dy,
                               head_width=0.15, head_length=0.1,
                               fc=color, ec=color, zorder=6, alpha=0.7)

    # Auto-scale limits based on data, but ensure at least [0, 10] range
    all_x = []
    all_y = []
    for points in trajectories:
        if points:
            all_x.extend([p[0] for p in points])
            all_y.extend([p[1] for p in points])
    
    if all_x and all_y:
        x_min_plot = min(0, min(all_x) - 0.5)
        x_max_plot = max(10, max(all_x) + 0.5)
        y_min_plot = min(0, min(all_y) - 0.5)
        y_max_plot = max(10, max(all_y) + 0.5)
    else:
        x_min_plot, x_max_plot = 0, 10
        y_min_plot, y_max_plot = 0, 10

    ax.set_xlim(x_min_plot, x_max_plot)
    ax.set_ylim(y_min_plot, y_max_plot)
    ax.set_aspect('equal', 'box')

    # Labels and title
    ax.set_xlabel('x₁', fontsize=12)
    ax.set_ylabel('x₂', fontsize=12)
    title = 'Trajectory Plot with Regions'
    if is_3d:
        title += ' (3D model, showing x₁-x₂ projection)'
    ax.set_title(title, fontsize=14)
    
    if len(trajectories) > 1 or any(trajectories):
        ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()