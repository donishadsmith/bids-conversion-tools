API
===

:mod:`bidsprep.logger`
---------------------------
Module setting up a logger.

.. currentmodule:: bidsprep.logger

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   setup_logger


:mod:`bidsprep.io`
---------------------------
Module for input/output operations on NIfTI files and images.

.. currentmodule:: bidsprep.io

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   load_nifti
   compress_image
   get_files
   get_nifti_header
   get_nifti_affine
   create_bids_file
   create_dataset_description
   save_dataset_description

:mod:`bidsprep.utils`
---------------------------
Module containing utility functions.

.. currentmodule:: bidsprep.utils

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   determine_slice_dim
   get_hdr_metadata
   get_n_slices
   get_tr
   create_slice_timing
   is_3d_img
   get_scanner_info
   is_valid_date
   get_date_from_filename
