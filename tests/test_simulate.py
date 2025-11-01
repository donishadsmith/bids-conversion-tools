import nibabel as nib, numpy as np, pytest

from bidsprep.simulate import create_affine, simulate_nifti_image, add_nifti_header


def test_create_affine():
    """Test for ``create_affine``."""
    affine = create_affine(
        xyz_diagonal_value=2, translation_vector=np.array([1, 1, 1, 1])
    )
    assert all(np.diagonal(affine) == np.array([2, 2, 2, 1]))
    assert all(affine[:, 3] == np.array([1, 1, 1, 1]))


@pytest.mark.parametrize(
    "affine",
    [
        None,
        create_affine(xyz_diagonal_value=1, translation_vector=np.array([1, 1, 1, 1])),
    ],
)
def test_simulate_nifti_image(affine):
    """Test for ``simulate_nifti_image``."""
    img = simulate_nifti_image(img_shape=(20, 20, 20, 20), affine=affine)
    assert isinstance(img, nib.Nifti1Image)
    if affine is not None:
        assert all(np.diagonal(img.affine) == np.array([1, 1, 1, 1]))


def test_add_nifti_header():
    """Test for ``add_nifti_header``."""
    affine = create_affine(
        xyz_diagonal_value=3, translation_vector=np.array([1, 1, 1, 1])
    )
    img = simulate_nifti_image(img_shape=(20, 20, 20, 20), affine=affine)
    img = add_nifti_header(img)
    assert isinstance(img, nib.Nifti1Image)
    assert all(np.array(img.header.get_zooms()) == np.array([3, 3, 3, 0]))
