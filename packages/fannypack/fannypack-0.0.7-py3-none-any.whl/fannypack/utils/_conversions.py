from typing import Callable, Dict, List, Tuple, TypeVar, Union, cast, overload

import numpy as np
import torch

# General Container template; used by all conversion functions
Container = TypeVar("Container", List, Tuple, Dict)


# Private conversion helper: recursively calls a conversion function on all inputs
# within any nested set of containers
@overload
def _convert(x: Container, convert: Callable) -> Container:
    pass


@overload
def _convert(
    x: Union[torch.Tensor, np.ndarray], convert: Callable
) -> Union[torch.Tensor, np.ndarray]:
    pass


def _convert(x, convert):
    if type(x) in (torch.Tensor, np.ndarray):
        # Convert plain arrays
        output = convert(x)
    elif type(x) == dict:
        # Convert dictionaries of values
        x = cast(dict, x)
        output = {}
        for key, value in x.items():
            output[key] = _convert(value, convert)
    elif type(x) == list:
        # Convert lists of values
        x = cast(list, x)
        output = [_convert(value, convert) for value in x]
    elif type(x) == tuple:
        # Convert tuples of values
        x = cast(tuple, x)
        output = tuple(_convert(value, convert) for value in x)
    else:
        assert False, f"Invalid datatype {type(x)}!"
    return output


@overload
def to_device(x: Container, device: torch.device, detach: bool = False,) -> Container:
    pass


@overload
def to_device(
    x: torch.Tensor, device: torch.device, detach: bool = False,
) -> torch.Tensor:
    pass


def to_device(x, device, detach=False):
    """Move a torch tensor, list of tensors, or dict of tensors to a different device.

    Args:
        x: (torch.Tensor, list, tuple, or dict) Tensor or container of tensors to move.
        device (torch.device): Target device.
        detach (bool, optional): If set, detaches tensors after moving. Defaults to
            False.

    Returns:
        torch.Tensor, list, tuple, or dict: Output, type will mirror input.
    """

    def convert(x):
        if detach:
            x = x.detach()
        return x.to(device)

    return _convert(x, convert)


@overload
def to_torch(x: Container, device: str = "cpu") -> Container:
    pass


@overload
def to_torch(x: np.ndarray, device: str = "cpu") -> torch.Tensor:
    pass


def to_torch(x, device="cpu", convert_doubles_to_floats=True):
    """Converts a numpy array, list of numpy arrays, or dict of numpy arrays
    for use in PyTorch.

    Args:
        x: (np.ndarray, list, tuple, or dict) Array or container of arrays to convert to
            torch tensors.
        device (torch.device, optional): Torch device to create tensors on. Defaults to
            `"cpu"`.
        convert_doubles_to_floats (bool, optional): If set, converts 64-bit floats to
            32-bit. Defaults to True.

    Returns:
        torch.Tensor, list, tuple, or dict: Output, type will mirror input.
    """

    def convert(x: np.ndarray):
        output = torch.from_numpy(x)
        if x.dtype == np.float64 and convert_doubles_to_floats:
            output = output.float()
        output = output.to(device)
        return output

    return _convert(x, convert)


@overload
def to_numpy(x: Container) -> Container:
    pass


@overload
def to_numpy(x: torch.Tensor) -> np.ndarray:
    pass


def to_numpy(x):
    """Converts a tensor, list of tensors, or dict of tensors for use in Numpy.

    Args:
        x: (torch.Tensor, list, tuple, or dict) Tensor or container of tensors to
            convert to numpy.

    Returns:
        np.ndarray, list, tuple, or dict: Output, type will mirror input.
    """

    def convert(x: torch.Tensor):
        output = x.detach().cpu().numpy()
        return output

    return _convert(x, convert)
