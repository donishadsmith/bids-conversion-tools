"""Module for input/output operations."""

import glob, os
from typing import Union

import nibabel as nib


def load_nifti(
    nifti_file_or_img: Union[str, nib.nifti1.Nifti1Image],
) -> nib.nifti1.Nifti1Image:
    """
    Load NIfTI image.

    Loads NIfTI image when not a ``Nifti1Image`` object or
    returns the image if already loaded in.

    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    Returns
    -------
    nib.nifti1.Nifti1Image
        The loaded in NIfTI image.
    """
    nifti_img = (
        nib.load(nifti_file_or_img)
        if isinstance(nifti_file_or_img, nib.nifti1.Nifti1Image)
        else nifti_file_or_img
    )

    return nifti_img


def compress_image(
    nifti_file_or_img: Union[str, nib.nifti1.Nifti1Image], remove_src_file: bool = False
) -> None:
    """
    Compresses a ".nii" image to a ".nii.gz" image.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path of the NIfTI image.

    remove_src_file: :obj:`bool`
        Deletes the original source image file.

    Returns
    -------
    None
    """
    img = nib.load(nifti_file_or_img)
    nib.save(img, nifti_file_or_img.replace(".nii", ".nii.gz"))

    if remove_src_file and isinstance(nifti_file_or_img, (str,)):
        os.remove(nifti_file_or_img)


def get_files(target_dir: str, ext: str) -> list[str]:
    """
    Gets files with a specific extension.

    Parameters
    ----------
    target_dir: :obj:`str`
        The target directory.

    ext: :obj:`str`
        The extension.

    Returns
    -------
    list[str]
        List of files with the extension specified by ``ext``.
    """
    return glob.glob(os.path.join(target_dir, f"*.{ext}"))


def get_nifti_header(nifti_file_or_img):
    """
    Get header from NIfTI image.

    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    Returns
    -------
    nib.nifti1.Nifti1Image
        The header from a NIfTI image.
    """
    return load_nifti(nifti_file_or_img).header


def get_nifti_affine(nifti_file_or_img):
    """
    Get the affine matrix from NIfTI image.

    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    Returns
    -------
    nib.nifti1.Nifti1Image
        The header from a NIfTI image.
    """
    return load_nifti(nifti_file_or_img).affine
