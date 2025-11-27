from pathlib import Path

import pandas as pd, pytest

from nifti2bids.bids import (
    create_bids_file,
    create_participant_tsv,
    create_dataset_description,
    save_dataset_description,
    presentation_log_to_bids,
)
from ._constants import BLOCK_DATA, EVENT_DATA


@pytest.mark.parametrize("dst_dir, remove_src_file", ([None, True], [True, False]))
def test_create_bids_file(nifti_img_and_path, dst_dir, remove_src_file):
    """Test for ``create_bids_file``."""
    _, img_path = nifti_img_and_path
    dst_dir = None if not dst_dir else img_path.parent / "test"
    if dst_dir:
        dst_dir.mkdir()

    bids_filename = create_bids_file(
        img_path,
        subj_id="01",
        desc="bold",
        remove_src_file=remove_src_file,
        dst_dir=dst_dir,
        return_bids_filename=True,
    )
    assert bids_filename
    assert Path(bids_filename).name == "sub-01_bold.nii"

    if dst_dir:
        dst_file = list(dst_dir.glob("*.nii"))[0]
        assert Path(dst_file).name == "sub-01_bold.nii"

        src_file = list(img_path.parent.glob("*.nii"))[0]
        assert Path(src_file).name == "img.nii"
    else:
        files = list(img_path.parent.glob("*.nii"))
        assert len(files) == 1
        assert files[0].name == "sub-01_bold.nii"


def test_create_dataset_description():
    """Test for ``create_dataset_description``."""
    dataset_desc = create_dataset_description(dataset_name="test", bids_version="1.2.0")
    assert dataset_desc.get("Name") == "test"
    assert dataset_desc.get("BIDSVersion") == "1.2.0"


def test_save_dataset_description(tmp_dir):
    """Test for ``save_dataset_description``."""
    dataset_desc = create_dataset_description(dataset_name="test", bids_version="1.2.0")
    save_dataset_description(dataset_desc, tmp_dir.name)
    files = list(Path(tmp_dir.name).glob("*.json"))
    assert len(files) == 1
    assert Path(files[0]).name == "dataset_description.json"


def test_create_participant_tsv(tmp_dir):
    """Test for ``create_participant_tsv``."""
    path = Path(tmp_dir.name)
    extended_path = path / "sub-01"
    extended_path.mkdir()

    df = create_participant_tsv(path, save_df=True, return_df=True)
    assert isinstance(df, pd.DataFrame)

    filename = path / "participants.tsv"
    assert filename.is_file()

    df = pd.read_csv(filename, sep="\t")
    assert df["participant_id"].values[0] == "sub-01"


def _create_presentation_logfile(dst_dir, design):
    dst_dir = Path(dst_dir)
    data = BLOCK_DATA if design == "block" else EVENT_DATA

    filename = dst_dir / f"{design}.txt"
    with open(filename, mode="w") as file:
        for line in data:
            file.write("\t".join(line) + "\n")


@pytest.mark.parametrize("experimental_design", ("block", "event"))
def test_presentation_log_to_bids(tmp_dir, experimental_design):
    """Test for ``presentation_log_to_bids``."""
    from pandas.testing import assert_frame_equal

    filename = Path(tmp_dir.name) / f"{experimental_design}.txt"
    _create_presentation_logfile(tmp_dir.name, experimental_design)

    if experimental_design == "block":
        expected_df = pd.DataFrame(
            {
                "onset": [1.0, 35.0],
                "duration": [14.0, 14.0],
                "trial_type": ["indoor", "indoor"],
            }
        )
        kwargs = {
            "presentation_log_or_df": filename,
            "trial_types": ["indoor"],
            "experimental_design": "block",
            "rest_block_code": "rest",
            "convert_to_seconds": ["Time"],
        }
    else:
        expected_df = pd.DataFrame(
            {
                "onset": [7.9107, 10.8965],
                "duration": [0.7058, 0.6720],
                "trial_type": ["incongruentright", "neutralleft"],
            }
        )
        kwargs = {
            "presentation_log_or_df": filename,
            "trial_types": ["incongruent", "neutral"],
            "experimental_design": "event",
            "convert_to_seconds": ["Time"],
        }

    df = presentation_log_to_bids(**kwargs)
    assert_frame_equal(df, expected_df)

    if experimental_design == "event":
        expected_df["response"] = ["hit", "hit"]
        df = presentation_log_to_bids(**kwargs, include_response=True)
