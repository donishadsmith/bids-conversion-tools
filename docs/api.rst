API
===

:mod:`nifti2bids.bids`
----------------------
Module for initializing and creating BIDs compliant files.

.. currentmodule:: nifti2bids.bids

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   create_bids_file
   create_dataset_description
   save_dataset_description
   create_participant_tsv

:mod:`nifti2bids.logging`
-------------------------
Module setting up a logger.

.. currentmodule:: nifti2bids.logging

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   setup_logger


:mod:`nifti2bids.io`
--------------------
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

:mod:`nifti2bids.metadata`
--------------------------
Module containing functions to extract metadata information
from NIfTIs.

.. currentmodule:: nifti2bids.metadata

.. autosummary::
   :template: function.rst
   :nosignatures:
   :toctree: generated/

   determine_slice_axis
   get_hdr_metadata
   get_n_volumes
   get_n_slices
   get_tr
   create_slice_timing
   is_3d_img
   get_scanner_info
   is_valid_date
   get_date_from_filename
   get_entity_value
   infer_task_from_image
