# Changelog

Documentation of changes for each version of ``Nifti2Bids``.

## [0.1.1] - 2025-11-10
- Add Philip's specific interleaved order and multiband slice acquisition
- Other paramete name changes

## [0.1.0] - 2025-11-06
- Change utils module name to metadata
- Change logger module name to logging
- Create new bids module and move ``create_bids_file``, ``create_dataset_description``, ``save_dataset_description``, and ``create_participant_tsv`` to it
- Add ``save_df`` and ``return_df`` parameters to ``create_participant_tsv``

## [0.0.9] - 2025-11-05
- Add ``slice_axis`` parameter to ``create_slice_timing``

## [0.0.8] - 2025-11-05
- Change function and parameter names ending in "dim" to "axis"
- Change custom exception name
- Add new function to infer task based on number of volumes
- Add level parameter to ``setup_logger``
- Rename package from ``BidsPrep`` to ``Nifti2Bids``

## [0.0.7] - 2025-11-05
- Add  ``get_n_volumes`` function and change custom exceptions names

## [0.0.6] - 2025-11-04
- Add exception to ``create_slice_timing`` for safety

## [0.0.5] - 2025-11-04
- Fix ``create_bids_filename`` to not add "desc"
- Return numeric values as regular Python integers and float
- Add function to extract entity value
- Change ``destination_dir`` and ``output_dir`` to ``dst_dir``

## [0.0.4] - 2025-11-04
- Add function to create participants tsv file.
- ``get_files`` changed to ``glob_contents``.

## [0.0.3] - 2025-11-04
- Add function for extracting date from filenames.

## [0.0.2] - 2025-11-04
- Change output of ``create_slice_timing`` from a dictionary to a list.

## [0.0.1] - 2025-11-03
- First non-alpha release of ``BIDSPrep``.
