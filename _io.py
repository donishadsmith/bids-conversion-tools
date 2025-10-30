"""Module for input/output operations."""

import glob, os
from typing import Optional, Union

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


def rename_file(src_file: str, dst_file: str, remove_src_file: bool) -> None:
    """
    Renames a file.

    Parameters
    ----------
    src_file: :obj:`str`
        The source file to be renamed

    dst_file: :obj:`str`
        The new file name.

    remove_src_file: :obj:`str`
        Delete the source file if True.

    Returns
    -------
    None
    """
    os.rename(src_file, dst_file)

    if remove_src_file:
        os.remove(src_file)

def create_bids_file(
    nifti_file: str,
    subj_id: Union[str, int],
    desc: str,
    ses_id: Optional[Union[str, int]] = None,
    task_id: Optional[str] = None,
    run_id: Optional[Union[str, int]] = None,
    remove_src_file: bool = False,
    return_bids_filename: bool = False,
) -> Union[str, None]:
    """
    Create a BIDS compliant filename with required and optional entities.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to NIfTI image.

    sub_id: :obj:`str` or :obj:`int`
        Subject ID (i.e. 01, 101, etc).

    desc: :obj:`str`
        Description of the file (i.e., T1w, bold, etc).

    ses_id: :obj:`str` or :obj:`int` or :obj:`None`, default=None
        Session ID (i.e. 001, 1, etc). Optional entity.

    ses_id: :obj:`str` or :obj:`int` or :obj:`None`, default=None
        Session ID (i.e. 001, 1, etc). Optional entity.

    task_id: :obj:`str` or :obj:`None`, default=None
        Task ID (i.e. flanker, n_back, etc). Optional entity.

    run_id: :obj:`str` or :obj:`int` or :obj:`None`, default=None
        Run ID (i.e. 001, 1, etc). Optional entity.

    remove_src_file: :obj:`str`
        Delete the source file if True.

    return_bids_filename: :obj:`str`
        Returns the BIDS filename if True.

    Returns
    -------
    None or str
        If ``return_bids_filename`` is True, then the BIDS filename is
        returned.

    Note
    ----
    There are additional entities that can be used that are
    not included in this function
    """
    bids_filename = (
        f"sub-{subj_id}_ses-{ses_id}_task-{task_id}_" f"run-{run_id}_desc-{desc}"
    )
    bids_filename = _strip_none_entities(bids_filename)

    ext = f".{nifti_file.partition('.')[-1]}"
    bids_filename += f"{ext}"

    rename_file(nifti_file, bids_filename, remove_src_file)

    return bids_filename if return_bids_filename else None


def _strip_none_entities(bids_filename: str) -> str:
    """
    Removes entities with None in a BIDS compliant filename
    ("sub-101_ses-None_task-flanker_desc-bold.nii.gz" ->
     "sub-101_task-flanker_desc-bold.nii.gz")
    Parameters
    ----------
    bids_filename: :obj:`str`
        The BIDS filename.

    Returns
    -------
    str
        BIDS filename with entities ending in None removed.

    Example
    -------
    >>> bids_filename = "sub-101_ses-None_task-flanker_desc-bold.nii.gz"
    >>> _strip_none_entities(bids_filename)
        "sub-101_task-flanker_desc-bold.nii.gz"
    """
    basename, _, ext = bids_filename.partition(".")
    retained_entities = [
        entity for entity in basename.split("_") if not entity.endswith("-None")
    ]

    return f"{'_'.join(retained_entities)}.{ext}"
