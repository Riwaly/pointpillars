# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/11_interference.ipynb (unless otherwise specified).

__all__ = ['logger', 'predict_single_pcd', 'bb_tensor_to_velodyne_coords', 'view_single_pcd_prediction']

# Cell
import torch
import logging

from .utils.io import read_config, load_network_save, load_single_pcd
from .data.dataset import VelTrainDataset, collate_fn
from .modules.pointpillars import PointPillars, init_weights
from .utils.pcviewer import PCViewer

# Cell
logger = logging.getLogger(__name__)


# Cell
def predict_single_pcd(pcd_nbr: int, net_save_name: str):
    """Create a network prediction from a saved network for a single point cloud"""

    vel_folder = "/home/qhs67/git/bachelorthesis_sven_thaele/code/data/kitti/training/velodyne/training"
    label_folder ="/home/qhs67/git/bachelorthesis_sven_thaele/code/data/kitti/training/label_2/training"

    dataset = VelTrainDataset(vel_folder, label_folder)
    batch_tuple = dataset[pcd_nbr]

    batch = []
    for i, tensor in enumerate(batch_tuple):
        tensor = tensor.unsqueeze(0)
        batch.append(tensor)

    pil_batch, ind_batch, label_batch = batch

    #pil_batch, ind_batch, label_batch, _ = collate_fn(batch)
    with torch.no_grad():
        conf = read_config()
        net_save = load_network_save(net_save_name)
        net = PointPillars(conf)
        net.load_state_dict(net_save)
        net.eval()
        net.cuda()

        pred_anchors, label_mask = net(pil_batch, ind_batch, label_batch)

    return pred_anchors, label_batch, label_mask

# Cell
def bb_tensor_to_velodyne_coords(bb_cam: torch.Tensor):
    xc, yc, zc, box_dims = bb_cam[:,0], bb_cam[:, 1], bb_cam[:, 2], bb_cam[:, 3:]

    xv = zc
    yv = -1 * xc
    zv = -1 * yc

    return torch.cat((xv.unsqueeze(1), yv.unsqueeze(1), zv.unsqueeze(1), box_dims), dim=1)


# Cell
def view_single_pcd_prediction(pcd_nbr: str, net_save_name: str):
    pcloud = load_single_pcd(pcd_nbr)
    pred_anchors, label_batch, label_mask = predict_single_pcd(int(pcd_nbr), net_save_name)

    #xp, yp, zp, rp = pcloud[:,0], pcloud[:,1], pcloud[:,2], pcloud[:,3]
    #pcloud = torch.stack((xp, yp, zp, rp), dim=1)
    #pcloud = torch.stack((zp, yp, xp, rp), dim=1)
    label_batch = label_batch[0]
    #pred_anchors = bb_tensor_to_velodyne_coords(pred_anchors)
    label_batch = bb_tensor_to_velodyne_coords(label_batch)

    PCViewer.view_pcd_from_network_output(pcloud, pred_anchors, label_batch)



