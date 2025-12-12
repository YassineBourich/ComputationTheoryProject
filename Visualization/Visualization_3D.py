import pybullet as p
import pybullet_data
import time
import math

"""
model = SymbolicModel(reachability, reach_method, X, U, W, Nx, Nu)
specification: ExampleSpecification_2D(model)

"""

base_colors = [[0.5, 1.0, 0.5, 0.8], [0.5, 0.8, 1.0, 0.8], [1.0, 0.7, 0.8, 0.8], [1.0, 0.4, 0.4, 0.9]]

def visualize_trajectory(Regions, trajectory, speed=0.02):
    client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=0, cameraPitch=-80, cameraTargetPosition=[5, 2, 0])
    p.setGravity(0, 0, -10)

    floor_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[20, 20, 0.1])
    floor_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[20, 20, 0.1], rgbaColor=[0.5, 0.5, 0.5, 1])
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=floor_shape, baseVisualShapeIndex=floor_visual,
                      basePosition=[5, 5, -0.1])

    num_regions = len(Regions.keys())
    colors = {i: base_colors[i % len(base_colors)] for i in range(num_regions)}

    for i, b in enumerate(Regions):
        x_min, y_min, x_max, y_max = b[0][0], b[0][1], b[1][0], b[1][1]
        w, h = (x_max - x_min) / 2, (y_max - y_min) / 2
        cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2
        s = p.createCollisionShape(p.GEOM_BOX, halfExtents=[w, h, 0.02])
        v = p.createVisualShape(p.GEOM_BOX, halfExtents=[w, h, 0.02], rgbaColor=colors[i])
        p.createMultiBody(baseMass=0, baseCollisionShapeIndex=s, baseVisualShapeIndex=v, basePosition=[cx, cy, 0.01],
                          baseOrientation=[0, 0, 0, 1])
        # p.addUserDebugText(text=f"R{i+1}", textPosition=[cx, cy, 0.1], textColorRGB=[0, 0, 0], textSize=1.5, lifeTime=0)

    cs = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.15, height=0.3)
    vs = p.createVisualShape(p.GEOM_CYLINDER, radius=0.15, length=0.3, rgbaColor=[1, 0, 0, 1.0])
    robot = p.createMultiBody(baseMass=1.0, baseCollisionShapeIndex=cs, baseVisualShapeIndex=vs,
                              basePosition=[trajectory[0][0], trajectory[0][1], 0.15], baseOrientation=[0, 0, 0, 1])

    step, dt = 0, 0.003 / speed
    while step < len(trajectory) and p.isConnected():
        x, y = trajectory[step]
        yaw = math.atan2(trajectory[step + 1][1] - y, trajectory[step + 1][0] - x) if step < len(trajectory) - 1 else 0
        q = p.getQuaternionFromEuler([0, 0, yaw])
        p.resetBasePositionAndOrientation(robot, [x, y, 0.15], q)
        if step < len(trajectory) - 1:
            x1, y1, x2, y2 = trajectory[step][0], trajectory[step][1], trajectory[step + 1][0], trajectory[step + 1][1]
            p.addUserDebugLine([x1, y1, 0.05], [x2, y2, 0.05], lineColorRGB=[1, 0, 0], lineWidth=2, lifeTime=0)
        p.stepSimulation()
        time.sleep(dt)
        step += 1

    print("Done. Close window to exit.")
    while p.isConnected():
        p.stepSimulation()
        time.sleep(0.1)
    if p.isConnected():
        p.disconnect()