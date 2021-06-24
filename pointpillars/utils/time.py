# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.time.ipynb (unless otherwise specified).

__all__ = ['time_method']

# Cell
import torch

# Cell
def time_method(method: object, runs: int = 1, kwargs: dict = None):
    """
        Method to time other methods. A number of runs can be defined, which results in giving the mean.

        param object: method name (without brackets)
        param runs: number of runs do
        param kwargs: method args in form of a dict, e.g. kwargs={"pcloud": pc}
        returns: mean time of the method runs in milli seconds
    """
    times = torch.empty(runs, dtype=torch.float)
    for i in range(runs):
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()

        if kwargs:
            method(**kwargs)
        else:
            method()

        end.record()
        torch.cuda.synchronize()
        times[i] = start.elapsed_time(end)

    return times.mean()