# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.box_ops.ipynb (unless otherwise specified).

__all__ = ['logger', 'convert_boxes_to_2d_corners', 'convert_boxes_to_3d_corners']

# Cell
import torch
import logging


# Cell
logger = logging.getLogger(__name__)

# Cell
def convert_boxes_to_2d_corners(boxes: torch.Tensor) -> torch.Tensor:
    """Converts center representation to bounding corners
    :param boxes: tensor(batch_size, nbr_boxes, nb_attributes)

    :returns: tensor(batch_size, max_nbr_pred_boxes, 4)
                with last dimension being (x_min, y_min, x_max, y_max)
    """
    logger.info("Converting boxes to corners...")
    logger.debug(f"boxes: {boxes}{boxes.shape}")

    xy = boxes[:,:,:2]
    wl = boxes[:,:,4:6]

    xy_min = xy - 0.5 * wl
    xy_max = xy + 0.5 * wl

    logger.debug(f"Boxes to corner convertion complete.\n"
                 f"xy_min: {xy_min}{xy_min.shape},\n"
                 f"xy_max: {xy_max}{xy_max.shape}")

    del xy, wl
    return torch.cat([xy_min, xy_max], dim=2)

# Cell
def convert_boxes_to_3d_corners(self, boxes: torch.Tensor) -> torch.Tensor:
    """Converts center representation to bounding corners"""
    pass
