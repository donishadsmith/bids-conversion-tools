"""Module for creating simulated data."""

import nibabel as nib, numpy as np

from numpy.typing import NDArray


def simulate_nifti_image(
    img_shape: tuple[int, int, int, int], affine: NDArray = None
) -> nib.Nifti1Image:
    """
    Simulate a NIfTI image.

    Parameters
    ----------
    img_shape: :obj:`tuple[int, int, int, int]`
        Shape of the NIfTI image.

    affine: :obj:`NDArray`, default=None
        The affine matrix. If None, the default affine matrix
        has uses "2" for the diagonal values with a translation
        of ``np.array([-96, -132, -78, 1])``.

    Returns
    -------
    Nifti1Image
        The NIfTI image.
    """
    if not affine:
        affine = _create_affine(
            diagonal_value=2, translate_vec=np.array([-96, -132, -78, 1])
        )

    return nib.Nifti1Image(np.random.rand(*img_shape), affine)


def _create_affine(diagonal_value: int, translation_vector: NDArray) -> NDArray:
    """
    Generate an 4x4 affine matrix.

    Parameters
    ----------
    diagonal_value: :obj:`int`
        The value assigned to the diagonal of the affine.

    translation_vector: :obj:`NDArray`
        The translation vector/shift from the origin.

    Returns
    -------
    NDArray
        The affine matrix.
    """
    affine = np.zeros((4, 4))
    np.fill_diagonal(affine[:3], diagonal_value)
    affine[:, 3:] = translation_vector[:, np.newaxis]

    return affine
