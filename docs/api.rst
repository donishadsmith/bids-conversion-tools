API
===

:mod:`nifti2bids.logger`
---------------------------
Module setting up a logger.

.. currentmodule:: nifti2bids.logger

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   setup_logger


:mod:`nifti2bids.io`
---------------------------
Module for input/output operations on NIfTI files and images.

.. currentmodule:: nifti2bids.io

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   load_nifti
   compress_image
   glob_contents
   get_nifti_header
   get_nifti_affine
   create_bids_file
   create_dataset_description
   save_dataset_description

:mod:`nifti2bids.utils`
---------------------------
Module containing utility functions.

.. currentmodule:: nifti2bids.utils

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   determine_slice_dim
   get_hdr_metadata
   get_n_volumes
   get_n_slices
   get_tr
   create_slice_timing
   is_3d_img
   get_scanner_info
   is_valid_date
   get_date_from_filename
   create_participant_tsv
   get_entity_value
   infer_task_from_image
