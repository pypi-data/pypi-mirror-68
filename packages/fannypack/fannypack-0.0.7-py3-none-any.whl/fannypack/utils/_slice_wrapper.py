from __future__ import annotations

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

import numpy as np
import torch

import fannypack

# Valid raw types that we can wrap
_raw_types = set([list, tuple, np.ndarray, torch.Tensor])

# Alias for dictionary types
DictType = Union[
    Dict[Any, List], Dict[Any, Tuple], Dict[Any, torch.Tensor], Dict[Any, np.ndarray],
]

# Alias for valid raw types that we can wrap
InputType = Union[List, Tuple, torch.Tensor, np.ndarray, DictType]


class SliceWrapper:
    """A thin wrapper class for creating a unified interface for...
    - Lists
    - Tuples
    - Torch tensors
    - Numpy arrays
    - Dictionaries containing a same-length group of any of the above

    This is primarily to make it easier to read, slice, and index into aligned blocks of
    time-series data organized as dictionaries, but we also expose an interface for
    calling `append` and `extend` on wrapped lists.
    """

    def __init__(self, data: InputType):
        self.data = data
        """list, tuple, torch.Tensor, np.ndarray, or dict: Wrapped data."""

        # Sanity checks
        if type(self.data) == dict:
            # Cast for type-checking
            data_dict = cast(dict, self.data)

            # Every value in the dict should have the same length & type
            content_length = None
            content_type = None
            for value in data_dict.values():
                assert content_length is None or len(value) == content_length
                assert content_type is None or type(value) == content_type
                content_length = len(value)
                content_type = type(value)
                assert content_type in _raw_types
        else:
            # Non-dictionary inputs
            assert type(data) in _raw_types, "Invalid datatype!"

        # Backwards-compatibility
        def convert_to_numpy():  # pragma: no cover
            self.data = self.map(np.asarray).data

        self.convert_to_numpy = fannypack.utils.deprecation_wrapper(
            "SliceWrapper.convert_to_numpy() is deprecated -- please use "
            "the functional SliceWrapper.map() interface instead!",
            convert_to_numpy,
        )

    def __getitem__(self, index: Any) -> Any:
        """Unified interface for indexing into our wrapped object.

        For iterables that are directly wrapped, this is equivalent to evaluating
        `data[index]`.

        For wrapped dictionaries, this returns a new (un-wrapped) dictionary with the
        index applied value-wise.
        Thus, an input of...
        ```
        SliceWrapper({
            "a": a,
            "b": b,
        })
        ```
        would return...
        ```
        {
            "a": a[index],
            "b": b[index],
        }
        ```

        Args:
            index (Any): Index. Can be a slice, tuple, boolean array, etc.

        Returns:
            Any: Indexed value. See overall function docstring.
        """
        if type(self.data) == dict:
            # Cast for type-checking
            data_dict = cast(dict, self.data)

            # Check that the index is sane
            # Allows use as a standard iterator, eg `for obj in SliceWrapper(...)`
            if type(index) == int and index >= len(self):
                raise IndexError

            # Construct & return output
            output = {}
            for key, value in data_dict.items():
                output[key] = value[index]
            return output
        elif type(self.data) in _raw_types:
            return self.data[index]
        else:
            assert False, "Invalid operation!"

    def __len__(self) -> int:
        """Unified interface for evaluating the length of a wrapped object.

        Equivalent to `SliceWrapper.shape[0]`.

        Returns:
            int: Length of wrapped object.
        """
        return self.shape[0]

    def append(self, other: Any) -> None:
        """Append to the end of our data object.

        Only supported for wrapped lists and dictionaries containing lists.

        For wrapped lists, this is equivalent to `data.append(other)`.

        For dictionaries, `other` should be a dictionary.
        Behavior example...
        ```
        # Data before append
        {"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]}

        # Value of other
        {"a": 5, "b": 3}

        # Data after append
        {"a": [1, 2, 3, 4, 5], "b": [5, 6, 7, 8, 3]}
        ```

        Args:
            other (Any): Object to append.
        """
        if type(self.data) == dict:
            assert type(other) == dict, "Appended object must be a dictionary"

            # Cast for type-checking
            data_dict = cast(dict, self.data)
            other_dict = cast(dict, other)

            for key, value in other_dict.items():
                if key in data_dict.keys():
                    assert (
                        type(data_dict[key]) == list
                    ), "Append is only supported for wrapped lists"
                    data_dict[key].append(value)
                else:
                    data_dict[key] = [value]
        elif type(self.data) is list:
            cast(List, self.data).append(other)
        else:
            assert False, "Append is only supported for wrapped lists"

    def extend(self, other: InputType) -> None:
        """Extend to the end of our data object.

        Only supported for wrapped lists and dictionaries containing lists.

        For wrapped lists, this is equivalent to `data.extend(other)`.

        For dictionaries, `other` should be a dictionary.
        Behavior example...
        ```
        # Data before extend
        {"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]}

        # Value of other
        {"a": [5], "b": [3]}

        # Data after extend
        {"a": [1, 2, 3, 4, 5], "b": [5, 6, 7, 8, 3]}
        ```

        Args:
            other (dict or list): Object to append.
        """
        if type(self.data) == dict:
            assert type(other) == dict

            # Cast for type-checking
            data_dict = cast(dict, self.data)
            other_dict = cast(dict, other)

            for key, value in other_dict.items():
                if key in data_dict.keys():
                    assert (
                        type(data_dict[key]) == list
                    ), "Extend is only supported for wrapped lists"
                    data_dict[key].extend(value)
                else:
                    data_dict[key] = value
        elif type(self.data) == list:
            cast(list, self.data).extend(other)
        else:
            assert False, "Extend is only supported for wrapped lists"

    def map(self, function: Callable[[Any], Any]) -> SliceWrapper:
        """Compute a new SliceWrapper, with a function applied to all values within
        our wrapped data object.

        For iterables that are directly wrapped, this is equivalent to evaluating:
        ```
        SliceWrapper(function(data))
        ```

        For dictionaries, `function` is applied value-wise.
        Thus, an input of...
        ```
        SliceWrapper({
            "a": a,
            "b": b,
        })
        ```
        would return...
        ```
        SliceWrapper({
            "a": function(a),
            "b": function(b),
        })
        ```

        Args:
            function (Callable): Function to map.
        """
        if type(self.data) == dict:
            # Cast for type-checking
            data_dict = cast(dict, self.data)

            # Construct output
            mapped_data_dict = {}
            for key, value in data_dict.items():
                mapped_data_dict[key] = function(value)
        else:
            mapped_data_dict = function(self.data)

        return SliceWrapper(mapped_data_dict)

    @property
    def shape(self) -> Tuple[int, ...]:
        """Unified interface for polling the shape of our wrapped object.

        For lists and tuples, this simply evaluates to `(len(data),)`.

        For Numpy arrays and torch tensors, we get `data.shape`.

        For dictionaries, we return a tuple containing all shared dimensions between
        our wrapped values, starting from the leftmost dimension.

        Args:

        Returns:
            Tuple[int, ...]:
        """
        if type(self.data) == dict:
            # Cast for type-checking
            data_dict = cast(dict, self.data)

            # Find longest shared shape prefix
            output: Tuple[int, ...]
            first = True
            for value in data_dict.values():
                shape = self._shape_helper(value)
                if first:
                    output = shape
                    first = False
                    continue

                for i in range(min(len(output), len(shape))):
                    if output[i] != shape[i]:
                        output = output[:i]
                        break

            return tuple(output)
        else:
            return self._shape_helper(self.data)

    @staticmethod
    def _shape_helper(data) -> Tuple[int, ...]:
        """Computes the shape of an object. `data.shape` for tensors and Numpy arrays,
        `(len(data))` for lists and tuples.
        """
        if type(data) in (torch.Tensor, np.ndarray):
            # Return full shape
            return data.shape
        elif type(data) in (list, tuple):
            # Return 1D shape
            return (len(data),)
        else:
            assert False, "Invalid operation!"
