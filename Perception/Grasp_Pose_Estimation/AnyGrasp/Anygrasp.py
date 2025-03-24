# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : Anygrasp.py
# @Time           : 2024-08-03 15:07:35
# @Author         : yk
# @Email          : yangkui1127@gmail.com
# @Description:   : AnyGrasp: Grasp pose estimation algorithm
"""

# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copy
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from graspnetAPI import GraspGroup
from gsnet import AnyGrasp
from PIL import Image
from utils import *
from yacs.config import CfgNode as CN

# from Robotics_API import Pose
from Utils import *


class Anygrasp:
    """A class for grasp pose estimation using AnyGrasp model.

    Attributes:
        cfgs: Configuration settings.
        grasping_model: Instance of AnyGrasp model.
        cam: Camera parameters.
    """

    def __init__(self, anygrasp_cfg, camera_cfg):
        """Initialize Anygrasp class with configurations.

        Args:
            cfgs: Configuration settings.
        """
        self.anygrasp_cfg = anygrasp_cfg
        self.camera_cfg = camera_cfg
        self.anygrasp_cfg.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), self.anygrasp_cfg.output_dir
        )
        self.anygrasp_cfg.checkpoint_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.anygrasp_cfg.checkpoint_path,
        )
        self.grasping_model = AnyGrasp(self.anygrasp_cfg)
        self.grasping_model.load_net()

    def Grasp_Pose_Estimation(
        self,
        points: np.ndarray,
        image: Image.Image,
        colors: np.ndarray,
        seg_mask: np.ndarray,
        bbox: Bbox,
        crop_flag: bool = False,
    ):
        """Calculate the optimal grasping pose.

        Args:
            points (np.ndarray): 3D point cloud data of the scene.
            image (np.ndarray): RGB image corresponding to the point cloud.
            colors (np.ndarray): Image numpy normalized array.
            seg_mask (np.ndarray): Object segmentation mask.
            bbox (Bbox): Bounding box of the object in the scene, typically defined by coordinates (x_min, y_min, x_max, y_max).
            crop_flag (bool, optional): If False, the point cloud will be cropped using the segmentation mask to focus only on the object of interest. Defaults to False.

        Returns:
            Pose: The best grasp pose of object in scene.
        """

        # If the sampling rate is less than 1, the point cloud is downsampled
        if self.anygrasp_cfg.sampling_rate < 1:
            points, indices = sample_points(points, self.anygrasp_cfg.sampling_rate)
            colors = colors[indices]

        # gg is a list of grasps of type graspgroup in graspnetAPI
        xmin = points[:, 0].min()
        xmax = points[:, 0].max()
        ymin = points[:, 1].min()
        ymax = points[:, 1].max()
        zmin = points[:, 2].min()
        zmax = points[:, 2].max()
        lims = [xmin, xmax, ymin, ymax, zmin, zmax]

        # Grasp prediction, return grasp group and point cloud
        gg, cloud = self.grasping_model.get_grasp(
            points,
            colors,
            lims,
            apply_object_mask=True,
            dense_grasp=False,
            collision_detection=True,
        )
        trans_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        cloud.transform(trans_mat)

        if len(gg) == 0:
            print(
                "[AnyGrasp] \033[33mwarning\033[0m: No Grasp detected after collision detection!"
            )
            return None

        # The grasped groups are subjected to non-maximum suppression (NMS) and sorted by scores.
        gg = gg.nms().sort_by_score()
        print(
            "[AnyGrasp] \033[34mInfo\033[0m: Grasp point number of all objects:",
            len(gg),
        )

        if self.anygrasp_cfg.debug:
            grippers = gg.to_open3d_geometry_list()
            for gripper in grippers:
                gripper.transform(trans_mat)
            visualize_cloud_geometries(
                cloud,
                grippers,
                save_file=os.path.join(self.anygrasp_cfg.output_dir, "poses.png"),
            )

        filter_gg = GraspGroup()

        # Reference direction vector, indicating the ideal grasping direction.
        # ref_vec = np.array([0, math.cos(self.camera_cfg.head_tilt), -math.sin(self.camera_cfg.head_tilt)])
        ref_vec = np.array([0, 0, 1])

        # visualize the grip points associated with the given object
        image = copy.deepcopy(image)
        img_drw = draw_rectangle(image, bbox)

        # Filtering the grasps by penalising the vertical grasps as they are not robust to calibration errors.
        for g in gg:

            grasp_center = g.translation

            # Convert the coordinates of a grasp center in three-dimensional space to two-dimensional coordinates on the image plane
            ix = max(
                0,
                min(
                    self.camera_cfg.width - 1,
                    int(
                        ((grasp_center[0] * self.camera_cfg.fx) / grasp_center[2])
                        + self.camera_cfg.cx
                    ),
                ),
            )
            iy = max(
                0,
                min(
                    self.camera_cfg.height - 1,
                    int(
                        ((-grasp_center[1] * self.camera_cfg.fy) / grasp_center[2])
                        + self.camera_cfg.cy
                    ),
                ),
            )

            if crop_flag:
                filter_gg.add(g)
            else:
                if seg_mask[
                    iy, ix
                ]:  # Check if the grasp point is within the grasp object area
                    img_drw.ellipse([(ix - 2, iy - 2), (ix + 2, iy + 2)], fill="green")

                    # # 3 * 3 rotation matrix
                    # rotation_matrix = g.rotation_matrix

                    # # The angle between ref vec and grasp z-axis direction
                    # cur_vec = rotation_matrix[:, 2]
                    # angle = math.acos(np.dot(ref_vec, cur_vec) / (np.linalg.norm(cur_vec)))

                    # score = g.score - 0.1 * (angle) ** 4

                    # if g.score >= 0.095:
                    #     g.score = score

                    filter_gg.add(g)
                else:
                    img_drw.ellipse([(ix - 2, iy - 2), (ix + 2, iy + 2)], fill="red")

        if len(filter_gg) == 0:
            print(
                "[AnyGrasp] \033[33mwarning\033[0m: No grasp poses detected for this object try to move the object a little and try again"
            )
            return None

        # show and save grasp projections result
        projections_file_name = os.path.join(
            self.anygrasp_cfg.output_dir, "grasp_projections.png"
        )
        if self.anygrasp_cfg.debug:
            plt.imshow(image)
            plt.title("visualize grasp projections")
            plt.axis("off")
            plt.show()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        cv2.imwrite(projections_file_name, image)
        print(
            f"[AnyGrasp] \033[34mInfo\033[0m: Saved projections of grasps at {projections_file_name}"
        )

        filter_gg = filter_gg.nms().sort_by_score()
        print(
            "[AnyGrasp] \033[34mInfo\033[0m: Filter grasp point number of grasp object:",
            len(filter_gg),
        )

        self.print_filter_gg(filter_gg)

        if self.anygrasp_cfg.debug:
            filter_grippers = filter_gg.to_open3d_geometry_list()
            for gripper in filter_grippers:
                gripper.transform(trans_mat)
            visualize_cloud_geometries(
                cloud,
                [filter_grippers[0].paint_uniform_color([1.0, 0.0, 0.0])],
                save_file=os.path.join(self.anygrasp_cfg.output_dir, "best_pose.png"),
            )

        best_pose = [filter_gg[0].translation, filter_gg[0].rotation_matrix]
        return best_pose

    def print_filter_gg(self, filter_gg):
        """print grasp pose and score, Descending.

        Args:
            filter_gg (): anygrasp grasp pose info
        """
        print(f"[AnyGrasp] \033[34mInfo\033[0m: AnyGrasp output pose about object:")
        for g in filter_gg:
            print(
                f"[AnyGrasp] \033[34mInfo\033[0m: translation: {g.translation}, z_vec: {g.rotation_matrix[:, 2]}, score: {g.score}"
            )


if __name__ == "__main__":

    # set work dir to AnyGrasp
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    input = deserialize("./data.pkl")
    anygrasp_cfg = input["anygrasp_cfg"]
    camera_cfg = input["camera_cfg"]
    points = input["points"]
    image = input["image"]
    colors = input["colors"]
    seg_mask = input["seg_mask"]
    bbox = input["bbox"]

    anygrasp = Anygrasp(anygrasp_cfg, camera_cfg)
    best_pose = anygrasp.Grasp_Pose_Estimation(points, image, colors, seg_mask, bbox)

    output = {
        "best_pose": best_pose,
    }
    serialize(output, "./data.pkl")
