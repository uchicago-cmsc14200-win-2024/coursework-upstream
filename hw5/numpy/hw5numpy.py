from abc import abstractmethod, ABC
from typing import Any

# type synonym for convenience
Shape = int | tuple[int, int]


class NDArray(ABC):
    """
    Abstract class for n-dimensional arrays
    """

    @property
    @abstractmethod
    def shape(self) -> Shape:
        """
        Return the shape of the data, either an int or a pair
        of ints in row, col order.

        Returns an int or a (row, col) pair of ints.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> list[int] | list[list[int]]:
        """
        Return *a defensive copy of* the data either as a list or
        list of lists.

        Don't return a reference to the actual data attribute
        itself so that it isn't subject to arbitrary modification.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def T(self) -> "NDArray":
        """
        Return the transpose of the data.

        Returns a 1D or 2D array. The tricky detail here is that
        in certain cases, an array changes dimension in
        transposition. The comments below address this.
        """
        raise NotImplementedError


class NDArray1(NDArray):
    """
    1-dimensional arrays
    """

    _data: list[int]
    _shape: Shape

    def __init__(self, data: list[int]):
        """
        Construct an NDArray1 from a list of int.
        """
        raise NotImplementedError

    def __add__(self, other: Any) -> "NDArray1":
        """
        Add either an int or another NDArray1.
        Produce a new array (functional style).

        Raises Value error if other is neither an int nor
        and NDArray1, or an NDArray1 of different shape.
        """
        raise NotImplementedError

    def __gt__(self, other: Any) -> list[bool]:
        """
        Return a list of bools indicating greater than given int.
        """
        raise NotImplementedError

    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is in the array.
        """
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray1 with the same shape and
        containing the same numbers.
        """
        raise NotImplementedError

    @property
    def shape(self) -> Shape:
        """
        see NDArray
        """
        raise NotImplementedError

    @property
    def data(self) -> list[int] | list[list[int]]:
        """
        see NDArray
        """
        raise NotImplementedError

    @property
    def T(self) -> NDArray:
        """
        see NDArray

        Note the transpose of a size-n 1D array is an nx1 2D array.
        """
        raise NotImplementedError


class NDArray2(NDArray):
    """
    2-dimensional arrays
    """

    _data: list[list[int]]
    _shape: Shape

    def __init__(self, data: list[list[int]]):
        """
        Construct an NDArray2 from a list of lists of int.

        Raises ValueError if list of lists is jagged (not
        rectangular).
        """
        raise NotImplementedError

    def __add__(self, other: Any) -> "NDArray2":
        """
        Add either an int or another NDArray2.
        Produce a new array (functional style).

        Raises Value error if other is neither and int nor an
        NDArray2, or an NDArray2 of different shape.
        """
        raise NotImplementedError

    def __gt__(self, other: Any) -> list[list[bool]]:
        """
        Return a list of lists of flags indicating greater than
        given int.
        """
        raise NotImplementedError

    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is anywhere in the array.
        """
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray2 with the same shape and
        containing the same numbers.
        """
        raise NotImplementedError

    @property
    def shape(self) -> Shape:
        """
        see NDArray
        """
        raise NotImplementedError

    @property
    def data(self) -> list[int] | list[list[int]]:
        """
        see NDArray
        """
        raise NotImplementedError

    @property
    def T(self) -> NDArray:
        """
        see NDArray

        Note the transpose of an nx1 2D array is a size-n 1D array.
        """
        raise NotImplementedError
