# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : open_drawer_pick_bowl_place_on_table_planning.py
# @Time           : 2024-10-25 20:29:19
# @Author         : why
# @Email          : wenhaoyu@mail.ustc.edu.cn
# @Description:   : A example to move bowl from drawer to table by arm and base planning entirely.
"""


import math
import os
import numpy as np

from Config import load_config
from Env import Client
from Motion_Planning.Manipulation.OMPL_Planner import OMPL_Planner
from Motion_Planning.Navigation import *
from Robotics_API import Bestman_sim_ur5e_vacuum_long, Pose
from SLAM import simple_slam
from Visualization import Visualizer

def pull_out(init_pose, i, distance):
    rotation_matrix = init_pose.get_orientation("rotation_matrix")
    front_direction = rotation_matrix[:, 0]
    new_position = np.array(init_pose.get_position()) - front_direction * i * distance
    return Pose(new_position, init_pose.get_orientation())

def main(filename):

    # Load config
    config_path = "Config/open_drawer_pick_bowl_place_on_table_planning.yaml"
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)

    # Load scene
    scene_path = "Asset/Scene/Scene/Kitchen_1.json"
    client.create_scene(scene_path)

    # Load bowl
    bowl_id = client.load_object(
        "bowl",
        "Asset/Scene/URDF_models/utensil_bowl_blue/model.urdf",
        [3.8, 2.4, 0.6],
        [0.0, 0.0, 0.0],
        1.0,
        False,
    )

    # Start record
    visualizer.start_record(filename)

    # Init robot
    bestman = Bestman_sim_ur5e_vacuum_long(client, visualizer, cfg)

    # Simple SLAM
    nav_obstacles_bounds = simple_slam(client, bestman, False)

    # Navigate to standing position
    nav_planner = AStarPlanner(
        robot_size=bestman.sim_get_robot_size(),
        obstacles_bounds=nav_obstacles_bounds,
        resolution=0.05,
        enable_plot=False,
    )

    standing_pose1 = Pose([2.7, 2.4, 0], [0.0, 0.0, 0.0])
    path = nav_planner.plan(bestman.sim_get_current_base_pose(), standing_pose1)
    bestman.sim_navigate_base(standing_pose1, path, enable_plot=True)

    # Draw drawer link
    visualizer.draw_aabb_link("elementA", 38)

    # Init planner
    ompl_planner = OMPL_Planner(bestman, cfg.Planner)

    # Get obstacles info
    ompl_planner.get_obstacles_info()

    # Get goal joint values
    min_x, min_y, min_z, max_x, max_y, max_z = client.get_link_bounding_box(
        "elementA", 38
    )

    # Get goal pose
    goal_pose = Pose(
        [min_x - bestman.sim_get_tcp_link_height()- 0.05, (min_y + max_y) / 2, (min_z + max_z) / 2], [0.0, 0.0, 0.0]
    )
    goal = ompl_planner.set_target_pose(goal_pose)

    # Open the drawer
    start = bestman.sim_get_current_joint_values()
    # planning path by RRT for suck drawer handle
    path = ompl_planner.plan(start, goal)
    bestman.sim_execute_trajectory(path, True)
    bestman.sim_create_movable_constraint("elementA", 38)

    # move backward for pull drawer
    bestman.sim_move_base_backward(0.2)

    # The end effector Move along the specified trajectory get effector to open the drawer further
    init_pose = bestman.sim_get_current_end_effector_pose()
    pull_joints = [
        bestman.sim_cartesian_to_joints(pull_out(init_pose, i, 0.004))
        for i in range(0, int(0.2/0.004)) # pull distance is 0.2
    ]
    bestman.sim_execute_trajectory(pull_joints, True)

    # remove constraint between end effector and drawer handle
    bestman.sim_remove_movable_constraint()

    # move backward for enough space to recovery init arm pose
    bestman.sim_move_base_backward(0.1)

    # init planner status and update obstacles info
    ompl_planner.__init__(bestman, cfg.Planner)

    # init arm pose
    bestman.sim_move_arm_to_joint_values(cfg.Robot.arm_init_jointValues)

    # move forward to pick next
    bestman.sim_move_base_forward(0.7)

    # Planning
    goal = ompl_planner.set_target("bowl")
    start = bestman.sim_get_current_joint_values()
    path = ompl_planner.plan(start, goal)

    # Robot execute, Reach object
    bestman.sim_execute_trajectory(path, enable_plot=True)

    # grasp target object
    bestman.sim_open_vacuum_gripper("bowl")

    # Come back to grasp init pose
    bestman.sim_execute_trajectory(path[::-1], enable_plot=True)

    ompl_planner.__init__(bestman, cfg.Planner)

    # Navigation to next pose
    standing_pose2 = Pose([1.0, 2, 0], [0.0, 0.0, -math.pi / 2])
    path = nav_planner.plan(bestman.sim_get_current_base_pose(), standing_pose2)
    bestman.sim_navigate_base(standing_pose2, path, enable_plot=True)

    # Move arm to table
    place_pose = Pose([1.0, 1.0, 1.0], [0.0, math.pi / 2.0, 0.0])

    # planning place pose trajectory and execute
    place_goal = ompl_planner.set_target_pose(place_pose)
    palce_start = bestman.sim_get_current_joint_values()
    path = ompl_planner.plan(palce_start, place_goal)
    bestman.sim_execute_trajectory(path, enable_plot=True)

    # place the bowl
    bestman.sim_close_vacuum_gripper()

    # init arm pose
    bestman.sim_move_arm_to_joint_values(cfg.Robot.arm_init_jointValues)
    # init planner status and update obstacles info
    ompl_planner.__init__(bestman, cfg.Planner)

    # End record
    visualizer.end_record()

    # disconnect
    client.wait(10)
    client.disconnect()


if __name__ == "__main__":

    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get current file name
    filename = os.path.splitext(os.path.basename(__file__))[0]

    main(filename)