from pathlib import Path
from typing import Optional

import pandas as pd

PRESENTATION_COLUMNS = [
    "Trial",
    "Event Type",
    "Code",
    "Time",
    "TTime",
    "Uncertainty",
    "Duration",
    "Uncertainty",
    "ReqTime",
    "ReqDur",
    "Stim Type",
    "Pair Index",
]


def _determine_deliminator(textlines: list[str], column_headers: list[str]) -> str:
    """
    Identify the deliminator used for the data based on the
    deliminator used for the column titles.

    Parameters
    ----------
    textlines: :obj:`list[str]`
        The lines of text from the presentation log file.

    column_headers: :obj:`list[str]` or :obj:`None`
        The column headers for the data in the Presentation log file.

    Returns
    -------
    str
        The deliminator
    """
    for line in textlines:
        if line.startswith(column_headers[0]):
            split_text = line.split(column_headers[1])[0]
            deliminator = split_text.removeprefix(column_headers[0])
            break

    return deliminator


def _convert_textlines_to_df(
    data_textlines: list[str], deliminator: str, column_headers
) -> pd.DataFrame:
    """
    Convert textlines to a Pandas Dataframe.

    Parameters
    ----------
    data_textlines: :obj:`list[str]`
        The lines of text containing the data.

    deliminator: :obj:`str`
        The seperator used for the data.

    column_headers: :obj:`list[str]` or :obj:`None`
        The column headers for the data in the Presentation log file.

    Returns
    -------
    Dataframe
        A Pandas dataframe of the data.
    """
    data = [line.removesuffix("\n").split(f"{deliminator}") for line in data_textlines]

    return pd.DataFrame(data, columns=column_headers)


def load_presentation_log(
    log_filepath: str | Path, column_headers: Optional[list[str]] = None
) -> pd.DataFrame:
    """
    Loads Presentation log file as a Pandas Dataframe.

    Parameters
    ----------
    log_filepath: :obj:`str` or :obj:`Path`
        Absolute path to the Presentation log file (i.e text, log, excel files).

    column_headers: :obj:`list[str]` or :obj:`None`, default=None
        The column headers for the data in the Presentation log file.
        If None, then the following headers are used:

        ::

            default_column_headers = [
                "Trial",
                "Event Type",
                "Code", "Time",
                "TTime",
                "Uncertainty",
                "Duration",
                "Uncertainty",
                "ReqTime",
                "ReqDur",
                "Stim Type",
                "Pair Index"
                ]


    Returns
    -------
    Dataframe
        A Pandas dataframe of the data.
    """
    with open(log_filepath, "r") as f:
        column_headers = column_headers if column_headers else PRESENTATION_COLUMNS
        textlines = f.readlines()
        deliminator = _determine_deliminator(textlines, column_headers)
        content_indices = []

        cleaned_textlines = [line for line in textlines if line != "\n"]
        for indx, line in enumerate(cleaned_textlines):
            # Get the starting index of the data columns
            if line.startswith(f"{deliminator}".join(column_headers)):
                content_indices.append(indx)
            # Get one more than the final index of the data colums
            # Note: the lines for the data contain a trial number
            elif content_indices and not line.split(f"{deliminator}")[0].isdigit():
                content_indices.append(indx)
                break

        start_indx = content_indices[0]
        stop_indx = (
            content_indices[1] if len(content_indices) > 1 else len(cleaned_textlines)
        )

        data_textlines = cleaned_textlines[(start_indx + 1) : stop_indx]

    return _convert_textlines_to_df(data_textlines, deliminator, column_headers)
