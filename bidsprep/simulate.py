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
        The affine matrix. If None, creates an identity matrix.

    Returns
    -------
    Nifti1Image
        The NIfTI image with no header.
    """
    if not affine:
        affine = create_affine(
            diagonal_value=1, translation_vector=np.array([0, 0, 0, 0])
        )

    return nib.Nifti1Image(np.random.rand(*img_shape), affine)


def add_nifti_header(nifti_image: nib.Nifti1Image) -> nib.Nifti1Image:
    """
    Adds a basic header to a NIfTI image.

    Parameters
    ----------
    nifti_image: :obj:`Nifti1Image`
        A NIfTI image.

    Returns
    -------
    Nifti1Image
        The NIfTI image with a header.
    """
    hdr = nib.Nifti1Header()
    hdr.set_data_shape(nifti_image.shape)

    # Assume isotropic
    hdr.set_xyzt_units(np.diagonal(nifti_image.affine)[0])
    hdr.set_data_dtype(nifti_image.get_fdata().dtype)

    return nib.Nifti1Image(nifti_image.get_fdata(), nifti_image.affine, header=hdr)


def create_affine(diagonal_value: int, translation_vector: NDArray) -> NDArray:
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
