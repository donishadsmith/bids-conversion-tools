"""General Utility Functions"""

from typing import Any, Literal, Optional, Union

import nibabel as nib, numpy as np

from ._decorators import check_all_none
from ._io import get_nifti_header
from ._logging import setup_logger

LGR = setup_logger()


class IncorrectSliceDimension(Exception):
    """
    Incorrect Slice Dimension.

    Raised when the number of slices does not match "slice_end" plus one.

    Parameters
    ----------
    slice_dim: :obj:`Literal["x", "y", "z"]`
        The specified slice dimension.

    n_slices: :obj:`int`
        The number of slices from the specified ``slice_dim``.

    slice_end: :obj:`int`
        The number of slices specified by "slice_end" in the NIfTI header.

    message: :obj:`str` or :obj:`None`:
        The error message. If None, a default error message is used.
    """

    def __init__(
        self,
        incorrect_slice_dim: Literal["x", "y", "z"],
        n_slices: int,
        slice_end: int,
        message: Optional[str] = None,
    ):
        if not message:
            self.message = (
                "Incorrect slice dimension. Number of slices for "
                f"{incorrect_slice_dim} dimension is {n_slices} but "
                f"'slice_end' in NIfTI header is {slice_end}."
            )
        else:
            self.message = message

        super().__init__(self.message)


@check_all_none(parameter_names=["nifti_file_or_img", "nifti_header"])
def determine_slice_dim(
    nifti_img: Optional[nib.nifti1.Nifti1Image] = None,
    nifti_header: Optional[nib.nifti1.Nifti1Header] = None,
) -> tuple[int, int]:
    """
    Determine the slice dimension

    Uses "slice_end" plus one to determine the likely slice dimension.

    Parameters
    ----------
    nifti_img: :obj:`Nifti1Image`
        A NIfTI image.

    Returns
    -------
    tuple[int, int]
        Tuple representing (slice_dim, slice_end)
    """
    if nifti_img:
        slice_end, hdr = get_hdr_metadata(
            nifti_file_or_img=nifti_img, metadata_name="slice_end", return_header=True
        )
    else:
        hdr = nifti_header
        slice_end = get_hdr_metadata(nifti_header=hdr, metadata_name="slice_end")

    if slice_end or np.isnan(slice_end):
        raise ValueError("'slice_end' metadata field not set.")

    slice_end = int(slice_end) + 1

    return np.where(hdr.get_data_shape() == slice_end)


@check_all_none(parameter_names=["nifti_file_or_img", "nifti_header"])
def get_hdr_metadata(
    metadata_name: str,
    nifti_file_or_img: Optional[Union[str, nib.nifti1.Nifti1Image]] = None,
    nifti_header: Optional[nib.nifti1.Nifti1Header] = None,
    return_header: bool = False,
) -> Union[Any, tuple[Any, nib.nifti1.Nifti1Header]]:
    """
    Get metadata from a NIfTI header.

    Parameters
    ----------
    metadata_name: :obj:`str`
        Name of the metadata field to return.

    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`, default=None
        Path to the NIfTI file or a NIfTI image. Must be specified
        if ``nifti_header`` is None.

    nifti_header: :obj:`Nifti1Header`, default=None
        Path to the NIfTI file or a NIfTI image. Must be specified
        if ``nifti_file_or_img`` is None.

    return_header: :obj:`bool`
        Returns the NIfTI header

    Returns
    -------
    Any or tuple[Any, nibabel.nifti1.Nifti1Header]
        If ``return_header`` is False, only returns the associated
        value of the metadata. If ``return_header`` is True returns
        a tuple containing the assoicated value of the metadata
        and the NIfTI header.
    """
    hdr = nifti_header if nifti_header else get_nifti_header(nifti_file_or_img)
    metadata_value = hdr.get(metadata_name)

    return metadata_value if not return_header else (metadata_value, hdr)


def get_n_slices(
    nifti_file_or_img: Union[str, nib.nifti1.Nifti1Image],
    slice_dim: Optional[Literal["x", "y", "z"]] = None,
) -> int:
    """
    Gets the number of slices from the header of a NIfTI image.

    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    slice_dim: :obj:`Literal["x", "y", "z"]` or :obj:`None`, default=None
        Dimension the image slices were collected in. If None,
        determines the slice dimension using metadata ("slice_end")
        from the NIfTI header.

    Returns
    -------
    int
        The number of slices.
    """
    slice_dim_map = {"x": 0, "y": 1, "z": 2}

    hdr = get_nifti_header(nifti_file_or_img)
    if slice_dim:
        slice_end = get_hdr_metadata(nifti_header=hdr, metadata_name="slice_end")
        n_slices = hdr.get_data_shape()[slice_dim_map[slice_dim]]
        if (not slice_end or np.isnan(slice_end)) and n_slices != slice_end + 1:
            raise IncorrectSliceDimension(slice_dim, n_slices, slice_end)

        slice_dim_indx = slice_dim_map[slice_dim]
    else:
        slice_dim_indx, _ = determine_slice_dim(nifti_header=hdr)

    return hdr.get_data_shape()[slice_dim_indx]


def get_tr(nifti_file_or_img: Union[str, nib.nifti1.Nifti1Image]) -> float:
    """
    Get the Repetition Time from the header of a NIfTI image.

    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    Returns
    -------
    float
        The repetition time.
    """
    hdr = get_nifti_header(nifti_file_or_img)

    if not (tr := hdr.get_zooms()[3]):
        LGR.critical(f"Suspicious repetition time: {tr}.")

    return tr


def flip_slice_order(slice_order, ascending: bool) -> list[int]:
    """
    Flip slice order.

    Parameters
    ----------
    slice_order: :obj:`list[int]`
        List containing integer values representing the slices.

    ascending: :obj:`bool`, default=True
        If slices were collected in ascending order (True) or descending
        order (False).

    Returns
    -------
    list[int]
        The order of the slices.
    """
    return np.flip(slice_order) if not ascending else slice_order


def create_sequential_order(n_slices: int, ascending: bool = True) -> list[int]:
    """
    Create index ordering for sequential acquisition method.

    Parameters
    ----------
    n_slices: :obj:`int`
        The number of slices.

    ascending: :obj:`bool`, default=True
        If slices were collected in ascending order (True) or descending
        order (False).

    Returns
    -------
    list[int]
        The order of the slices.
    """
    slice_order = list(range(0, n_slices))

    return flip_slice_order(slice_order, ascending)


def create_interleaved_order(n_slices: int, ascending: bool = True) -> list[int]:
    """
    Create index ordering for interleaved acquisition method.

    Parameters
    ----------
    n_slices: :obj:`int`
        The number of slices.

    ascending: :obj:`bool`, default=True
        If slices were collected in ascending order (True) or descending
        order (False).

    Returns
    -------
    list[int]
        The order of the slices.
    """
    slice_order = list(range(0, n_slices, 2)) + list(range(1, n_slices, 2))

    return flip_slice_order(slice_order, ascending)


def create_slice_timing(
    nifti_file_or_img: Union[str, nib.nifti1.Nifti1Image],
    slice_acquisition_method: Literal["sequential", "interleaved"],
    ascending: bool = True,
) -> dict[int, float]:
    """
    Parameters
    ----------
    nifti_file_or_img: :obj:`str` or :obj:`Nifti1Image`
        Path to the NIfTI file or a NIfTI image.

    slice_acquisition_method: :obj:`Literal["sequential", "interleaved"]`
        Method used for acquiring slices.

    ascending: :obj:`bool`, default=True
        If slices were collected in ascending order (True) or descending
        order (False).

    Returns
    -------
    dict[int, float]
        Dictionary mapping the slice number to the time the slice was aquired.
    """
    slice_ordering_func = {
        "sequential": create_sequential_order,
        "interleaved": create_interleaved_order,
    }

    tr = get_tr(nifti_file_or_img)
    n_slices = get_n_slices(nifti_file_or_img)

    slice_duration = tr / n_slices
    slice_order = slice_ordering_func[slice_acquisition_method](n_slices, ascending)
    slice_timing = np.linspace(0, tr - slice_duration, n_slices)[slice_order]

    return {k: v for k, v in zip(range(0, n_slices), slice_timing.tolist())}


def get_subject_id(nifti_file: str) -> str:
    """
    Determines the subject ID from a ``nifti_file``.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to the NIfTI file.
    """
    pass


def get_date(nifti_file: str) -> str:
    """
    Determines the date from a ``nifti_file``.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to the NIfTI file.
    """
    pass


def get_task(nifti_file: str) -> str:
    """
    Determines the task from a ``nifti_file``.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to the NIfTI file.
    """
    pass


def get_session(nifti_file: str) -> str:
    """
    Determines the session from a ``nifti_file``.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to the NIfTI file.
    """
    pass


def is_t1w(nifti_file: str) -> bool:
    """
    Determines if ``nifti_file`` is a T1w image.

    Parameters
    ----------
    nifti_file: :obj:`str`
        Path to the NIfTI file.
    """
    return "mprage" in nifti_file
