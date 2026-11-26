import math

import numpy as np
from numpy.linalg import inv


def compute_focal_length(width, height, f35):
    fx = fy = f35 * (math.sqrt(width**2 + height**2) / math.sqrt(36**2 + 24**2))
    return fx, fy


def compute_principal_point(width, height):
    cx = (width-1) / 2
    cy = (height-1) / 2
    return cx, cy


def compute_intrinsic_matrix(fx, fy, cx, cy, s=0):
    k= np.array([
        [fx, s, cx], 
        [0, fy, cy], 
        [0, 0, 1]
    ])
    return k


def normalise_camera_coordinates(k, u, v):
    return inv(k) @ np.array([u, v, 1])


def compute_projection_matrix(k, r, t):
    return k @ np.hstack((r, t.reshape(3, 1)))


def project_points(k, r, t, points_3d):
    points_camera = points_3d @ r.T + t.reshape(3)
    points_image = points_camera @ k.T

    return points_image[:, :2] / points_image[:, 2:3]


def compute_camera_centre(r, t):
    return -r.T @ t


