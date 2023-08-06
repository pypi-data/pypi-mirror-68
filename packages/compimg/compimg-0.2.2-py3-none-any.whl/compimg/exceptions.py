"""compimg exceptions module"""
import numpy as np

from typing import Sequence


class DifferentShapesError(Exception):
    def __init__(self, shape1: Sequence[int], shape2: Sequence[int]):
        super().__init__(f"Images have different shapes: {shape1} != {shape2}.")


class DifferentDTypesError(Exception):
    def __init__(self, dtype1: np.dtype, dtype2: np.dtype):
        super().__init__(
            f"Images have different dtypes: {dtype1.name} != {dtype2.name}."
        )


class NegativePadAmountError(Exception):
    def __init__(self, amount):
        super().__init__(f"Pad cannot be negative value like {amount}.")


class KernelBiggerThanImageError(Exception):
    def __init__(self, kernel_shape: Sequence[int], image_shape: Sequence[int]):
        super().__init__(
            f"\nKernel used in convolution must be bigger that image itself."
            f"Kernel shape = {kernel_shape}, Image shape = {image_shape}"
        )


class KernelShapeNotOddError(Exception):
    def __init__(self, kernel_shape: Sequence[int]):
        super().__init__(
            f"\nKernel used in convolution must be of odd shape. "
            f"Kernel shape = {kernel_shape}, rows and columns must be odd."
        )


class KernelNot2DArray(Exception):
    def __init__(self, dims: int):
        super().__init__(f"\nKernel must be 2D numpy array, not {dims}D.")
