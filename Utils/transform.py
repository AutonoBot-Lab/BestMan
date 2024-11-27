import numpy as np
import math
import pybullet as p
from Robotics_API import Pose

def get_length(vec, norm=2):
    """
    Compute the length (norm) of a given vector.
    """
    return np.linalg.norm(vec, ord=norm)

def get_unit_vector(vec):
    """
    Compute the unit vector (normalized vector) of the given vector.
    """
    norm = get_length(vec)
    if norm == 0:
        return vec
    return np.array(vec) / norm

def quat_from_axis_angle(axis, angle):
    """
    Generate a quaternion from an axis-angle representation of a rotation.

    Args:
        axis (array-like): The vector representing the rotation axis.
        angle (float): The rotation angle in radians.

    Returns:
        array: The computed quaternion (a 4-element array).
    """
    return np.append(math.sin(angle/2) * get_unit_vector(axis), [math.cos(angle / 2)])

def euler_from_quat(quat):
    return p.getEulerFromQuaternion(quat)

def quat_from_euler(euler):
    return p.getQuaternionFromEuler(euler) # TODO: extrinsic (static) vs intrinsic (rotating)

def invert(pose):
    pos, quat = pose.get_pose()
    return p.invertTransform(pos, quat)

def multiply(*poses):
    pose = poses[0].get_pose()[0]
    for next_pose in poses[1:]:
        pose = p.multiplyTransforms(pose[0], pose[1], *(next_pose.get_pose()))
    return pose