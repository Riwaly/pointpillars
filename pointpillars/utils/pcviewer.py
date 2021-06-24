# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.pcviewer.ipynb (unless otherwise specified).

__all__ = ['PCViewer', 'img_nbr', 'velodyne_location']

# Cell
import torch
import math
import numpy as np
import open3d as o3d

#from pointpillars.utils.box_ops import convert_boxes_to_3d_corners

# Cell
class PCViewer(object):

    def __init__(self):
        pass

    @staticmethod
    def view_pc_with_jupyter():
        """
        Visualize the point cloud on Jupyter Notebook.
        """
        pass

    @staticmethod
    def line_set_from_3d_box(box: np.ndarray, color: list) -> o3d.geometry.LineSet:
        """

        :param box: Tensor(1,7) with x,y,z,h,w,l,theta
        :param colors: list [3] with the rgb values between 0 and 1
        :return: LineSet as bounding box
        """
        x, y, z, h, w, l, theta = box.tolist()

        dh = 0.5 * h
        dw = 0.5 * w
        dl = 0.5 * l

        p0 = [x - dl, y + dw, z - dh]
        p1 = [x - dl, y - dw, z - dh]
        p2 = [x + dl, y - dw, z - dh]
        p3 = [x + dl, y + dw, z - dh]
        p4 = [x - dl, y + dw, z + dh]
        p5 = [x - dl, y - dw, z + dh]
        p6 = [x + dl, y - dw, z + dh]
        p7 = [x + dl, y + dw, z + dh]

        points = [p0, p1, p2, p3, p4, p5, p6, p7]
        #points = PCViewer.rotate_points_around_z(points, theta)
        # indices which corners have a connection with each other
        lines = [[0, 1], [0, 3], [2, 1], [2, 3], [4, 7], [4, 5], [6, 5], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

        colors = [color for i in range(len(lines))]

        line_set = o3d.geometry.LineSet()
        line_set.points =  o3d.utility.Vector3dVector(points)
        line_set.lines =  o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)


        return line_set

    @staticmethod
    def rotate_points_around_z(points: list, theta: float):
        """
        Rotates corner points by an angle theta around the z axes.
        The formulas are: Rv = (xcos(theta) - ysin(theta))e_x + (xsin(theta) + ycos(theta))e_y

        :param points: a list containing all points in format [[x1,y1,z1], [x2, y2, z2], ...]
        :param theta: angle by which to rotate. Given in rad.

        :returns: list containing the newly rotated points in format [[xn1, yn1, z1], [xn2, yn2, z2], ...]
        """
        for i, point in enumerate(points):
            x, y, z = point

            x_new = x * math.cos(theta) - y * math.sin(theta)
            y_new = x * math.sin(theta) + y * math.cos(theta)

            point = [x_new, y_new, z]
            points[i] = point

        return points

    @staticmethod
    def view_pcd_from_network_output(pcloud: torch.Tensor, pred_boxes: torch.Tensor, gt_boxes: torch.Tensor):
        """
        #TODO: Confirm dimension order from points
        :param pcloud: Tensor(nb_points, 4) with last dim being x,y,z,r
        :param pred_boxes: Tensor(nb_pred_boxes, 7) with last dim being x,y,z,h,w,l,theta
        :param gt_boxes: Tensor(nb_gt_boxes, 7) with last dim being x,y,z,h,w,l,theta
        :return:
        """
        pcloud = pcloud.cpu()
        pred_boxes = pred_boxes.cpu()
        gt_boxes = gt_boxes.cpu()

        pcloud = pcloud.numpy()
        pred_boxes = pred_boxes.numpy()
        gt_boxes = gt_boxes.numpy()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.open3d.utility.Vector3dVector(pcloud[:,:3])

        pred_boxes_arr = []
        for i, pred_box in enumerate(pred_boxes):
            pred_line_set = PCViewer.line_set_from_3d_box(pred_box, [1,0,0])
            pred_boxes_arr.append(pred_line_set)

        gt_boxes_arr = []
        for i, gt_box in enumerate(gt_boxes):
            gt_line_set = PCViewer.line_set_from_3d_box(gt_box, [0,1,0])
            gt_boxes_arr.append(gt_line_set)

        geometries = pred_boxes_arr + gt_boxes_arr
        #geometries = gt_boxes_arr
        geometries.append(pcd)
        o3d.visualization.draw_geometries(geometries)



# Cell
img_nbr = '000100'
velodyne_location = '/home/qhs67/git/bachelorthesis_sven_thaele/code/data/kitti/training/velodyne/training/{}.bin'.format(img_nbr)