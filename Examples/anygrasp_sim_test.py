# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : load_kitchen.py
# @Time           : 2024-08-03 15:04:25
# @Author         : yk
# @Email          : yangkui1127@gmail.com
# @Description:   : A example to load kitchen
"""

import math
import os
import pickle

import numpy as np

from Config import load_config
from Env import Client
from Motion_Planning.Manipulation.OMPL_Planner import OMPL_Planner

# from Perception.Grasp_Pose_Estimation import Anygrasp
# from Perception.Object_detection import Lang_SAM
from Robotics_API import Bestman_sim_panda_with_gripper, Pose
from Utils import *
from Visualization import Visualizer


def main():

    # Load config
    config_path = "Config/anygrasp_sim_test.yaml"
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)

    # Load scene
    scene_path = "Asset/Scene/Scene/Kitchen_anygrasp.json"
    client.create_scene(scene_path)

    # Init robot
    bestman = Bestman_sim_panda_with_gripper(client, visualizer, cfg)
    eef_pose = bestman.sim_get_current_eef_pose()
    eef_pose.print("init end effector pose")
    visualizer.draw_pose(eef_pose)

    # Debug, look for rgb and depth
    # bestman.sim_get_camera_rgb_image(False, True, "rgb_test")
    # bestman.sim_get_camera_depth_image(False, True, "depth_test")
    # bestman.sim_visualize_camera_3d_points()

    # debug, look for camera pose
    camera_pose = bestman.sim_get_camera_pose()
    visualizer.draw_pose(camera_pose)

    # Lang SAM object segment
    query = str(
        input("[Lang_SAM] \033[34mInfo: Enter a Object name in the image: \033[0m")
    )
    lang_sam = Submodule()
    lang_sam.add("query", query)
    lang_sam.add("input_img", bestman.camera.image)
    lang_sam.add("box_filename", "./output/sim_test/box.png")
    lang_sam.add("mask_filename", "./output/sim_test/mask.png")
    lang_sam.call(
        "lang-segment-anything", "Perception/Semantic_Segmentation/Lang_SAM/Lang_SAM.py"
    )
    seg_mask = lang_sam.get("seg_mask", np.ndarray)
    bbox = lang_sam.get("bbox", np.ndarray)

    # AnyGrasp pose estimation
    points, colors = bestman.sim_get_camera_3d_points()
    anygrasp = Submodule()
    anygrasp.add("anygrasp_cfg", cfg.Grasp_Pose_Estimation.AnyGrasp)
    anygrasp.add("camera_cfg", cfg.Camera)
    anygrasp.add("points", points)
    anygrasp.add("image", bestman.camera.image)
    anygrasp.add("colors", colors)
    anygrasp.add("seg_mask", seg_mask)
    anygrasp.add("bbox", bbox)
    anygrasp.call("anygrasp", "Perception/Grasp_Pose_Estimation/AnyGrasp/Anygrasp.py")
    best_pose = anygrasp.get("best_pose")
    print(best_pose)

    # anygrasp = Anygrasp(cfg.Grasp_Pose_Estimation.AnyGrasp)
    # print(type(cfg.Grasp_Pose_Estimation.AnyGrasp))
    # print(cfg.Grasp_Pose_Estimation.AnyGrasp)
    # best_pose = anygrasp.Grasp_Pose_Estimation(bestman.camera, seg_mask, bbox)
    # print(type(best_pose))
    # print(best_pose)
    # best_pose = bestman.sim_trans_camera_to_world(best_pose)
    # best_pose = bestman.align_grasp_pose_to_tcp([0, 0, -1], best_pose)
    # visualizer.draw_pose(best_pose)

    # Init ompl
    # ompl_planner = OMPL_Planner(bestman, cfg.Planner)
    # goal = ompl_planner.set_target_pose(best_pose)
    # ompl_planner.remove_obstacle("banana")
    # start = bestman.get_current_joint_values()
    # path = ompl_planner.plan(start, goal)
    # bestman.execute_trajectory(path, enable_plot=True)

    # bestman.sim_open_gripper()
    # bestman.sim_move_eef_to_goal_pose(best_pose, 50)
    # visualizer.draw_link_pose(bestman.sim_get_arm_id(), bestman.sim_get_eef_link())
    # bestman.pick(best_pose)
    # tmp_position = best_pose.get_position()
    # tmp_pose = Pose(
    #     [tmp_position[0], tmp_position[1], tmp_position[2] + 0.4],
    #     best_pose.get_orientation(),
    # )
    # bestman.sim_move_eef_to_goal_pose(tmp_pose, 50)

    # client.wait(5)
    # bestman.sim_close_gripper()

    # disconnect pybullet
    client.wait(100)
    client.disconnect()


if __name__ == "__main__":

    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()
