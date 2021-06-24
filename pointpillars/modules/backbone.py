# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_modules.backbone.ipynb (unless otherwise specified).

__all__ = ['logger', 'Backbone']

# Cell
import logging
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

# Cell
class Backbone(nn.Module):
    def __init__(self, fnet_cfg):
        super(Backbone, self).__init__()

        C = fnet_cfg.getint("nb_channels")
        # For cars: S = 2, for pedestrians: S = 1
        S = 2

        # Block1 (S, L, F) = (S, 4, C)
        self.block1 = self._conv_block(C, C, 1, S, 4)
        # Block2 (S, L, F) = (2S, 6, 2C)
        self.block2 = self._conv_block(C, 2*C, S, 2*S, 6)
        # Block3 (S, L, F) = (4S, 6, 4C)
        self.block3 = self._conv_block(2*C, 4*C, 2*S, 4*S, 6)

        # Up1 (S_in, S_out, F) = (S, S, 2C)
        self.up1 = self._up_block(C, 2*C, 1)
        # Up2 (S_in, S_out, F) = (2S, S, 2C)
        self.up2 = self._up_block(2*C, 2*C, 2)
        # Up3 (S_in, S_out, F) = (4S, S, 2C)
        self.up3 = self._up_block(4*C, 2*C, 4)

    def _conv_block(self, C_in: int, C_out: int, S_in: int, S_out: int, L: int):
        """Generates a convolution block, which consists of L individual blocks, all working on stride S_out
           in respect to the input stride. They output C_out number of channels. After each convolution we
           also apply BatchNorm and ReLU."""

        modules = []
        for i in range(L):
            if i == 0:
                modules.append(nn.Conv2d(C_in, C_out, 3, stride=int(S_out/S_in), padding=1))
            else:
                modules.append(nn.Conv2d(C_out, C_out, 3, padding=1))

            modules.append(nn.BatchNorm2d(C_out, ))
            modules.append(nn.ReLU(inplace=True))

        return nn.Sequential(*modules)

    def _up_block(self, C_in: int, C_out: int, stride: int):
        """Returns umsampling block (transposed Conv2D) with BatchNorm and ReLU applied thereafter."""
        return nn.Sequential(
            nn.ConvTranspose2d(C_in, C_out, stride, stride=stride),
            nn.BatchNorm2d(C_out),
            nn.ReLU(inplace=True)
        )

    def forward(self, batch: torch.tensor):
        """Applies the previously created layers in the correct order."""
        # block1
        batch = self.block1(batch)
        batch_up1 = self.up1(batch)

        # block2
        batch = self.block2(batch)
        batch_up2 = self.up2(batch)

        # block3
        batch = self.block3(batch)
        batch_up3 = self.up3(batch)

        batch = torch.cat([batch_up1, batch_up2, batch_up3], dim=1)
        del batch_up1, batch_up2, batch_up3

        return batch
