import csv, io
from pathlib import Path

import pandas as pd


def _determine_delimiter(
    textlines: list[str], initial_column_headers: tuple[str]
) -> str:
    """
    Identify the delimiter used for the data based on the
    delimiter used for the inital column headers.

    Parameters
    ----------
    textlines: :obj:`list[str]`
        The lines of text from the presentation log file.

    initial_column_headers: :obj:`tuple[str]`
        The initial column headers for data.

    Returns
    -------
    str
        The delimiter
    """
    sniffer = csv.Sniffer()
    for indx, line in enumerate(textlines):
        if line.startswith(tuple(initial_column_headers)):
            header_string = textlines[indx]

    return sniffer.sniff(header_string, delimiters=None).delimiter


def _convert_time(
    df: pd.DataFrame, convert_to_seconds: list[str], divisor: int
) -> pd.DataFrame:
    """
    Change time resolution of specific columns.

    Parameters
    ----------
    presentation_df: :obj:`DataFrame`
        Pandas Dataframe of the Presentation log

    convert_to_seconds: :obj:`list[str]` or :obj:`None`, default=None
        Columns to convert to time.

    divisor: :obj:`int` or :obj:`None`, default=None
        Value to divide columns listed in ``convert_to_columns`` by.

    Returns
    -------
    pandas.Dataframe
        Dataframe with timing of the columns listed in
        ``convert_to_seconds`` converted to the units
        of the ``divisor``floats and time resolution
    """
    convert_to_seconds = (
        [convert_to_seconds]
        if isinstance(convert_to_seconds, str)
        else convert_to_seconds
    )
    df[convert_to_seconds] = df[convert_to_seconds].apply(
        lambda x: x.astype(str).str.lower()
    )
    df[convert_to_seconds] = df[convert_to_seconds].replace("null", "nan")
    df[convert_to_seconds] = df[convert_to_seconds].replace("", "nan")
    df[convert_to_seconds] = df[convert_to_seconds].astype(float)
    df[convert_to_seconds] = df[convert_to_seconds].apply(lambda x: x / divisor)

    return df


def load_presentation_log(
    log_filepath: str | Path,
    convert_to_seconds: list[str] = None,
    initial_column_headers: tuple[str] = ("Trial", "Event Type"),
) -> pd.DataFrame:
    """
    Loads Presentation log file as a Pandas Dataframe.

    Parameters
    ----------
    log_filepath: :obj:`str` or :obj:`Path`
        Absolute path to the Presentation log file (i.e text, log, Excel files).

    convert_to_seconds: :obj:`list[str]` or :obj:`None`, default=None
        Convert the time resolution of the specified columns from 0.1ms to seconds.

    initial_column_headers: :obj:`tuple[str]`, default=("Trial", "Event Type")
        The initial column headers for data.

    Returns
    -------
    pandas.Dataframe
        A Pandas dataframe of the data.
    """
    with open(log_filepath, "r") as f:
        initial_column_headers = tuple(initial_column_headers)
        textlines = f.readlines()
        delimiter = _determine_delimiter(textlines, initial_column_headers)
        content_indices = []
        cleaned_textlines = [line for line in textlines if line != "\n"]
        for indx, line in enumerate(cleaned_textlines):
            # Get the starting index of the data columns
            if line.startswith(f"{delimiter}".join(initial_column_headers)):
                content_indices.append(indx)
            # Get one more than the final index of the data colums
            # Note: the lines for the data contain a trial number
            elif content_indices and not line.split(f"{delimiter}")[0].isdigit():
                content_indices.append(indx)
                break

        start_indx = content_indices[0]
        stop_indx = (
            content_indices[1] if len(content_indices) > 1 else len(cleaned_textlines)
        )

        text = "".join(cleaned_textlines[start_indx:stop_indx])
        df = pd.read_csv(io.StringIO(text, newline=None), sep=delimiter)

    return (
        df
        if not convert_to_seconds
        else _convert_time(df, convert_to_seconds, divisor=10000)
    )


def load_eprime_log(
    log_filepath: str | Path,
    convert_to_seconds: list[str] = None,
    drop_columns: list[str] = None,
    initial_column_headers: tuple[str] = ("ExperimentName", "Subject"),
) -> pd.DataFrame:
    """
    Loads EPrime 3 log file as a Pandas Dataframe.

    .. important::
       When EPrime 3 file is exported to text, remove the checkmark from
       the "Unicode" field. The type of text file the Edat file is exported
       as is irrelevent.

    Parameters
    ----------
    log_filepath: :obj:`str` or :obj:`Path`
        Absolute path to the Presentation log file (i.e text, log, excel files).

    convert_to_seconds: :obj:`list[str]` or :obj:`None`, default=None
        Convert the time resolution of the specified columns from milliseconds to seconds.

    drop_columns: :obj:`list[str]` or :obj:`None`, default=None
        Remove specified columns from dataframe.

    initial_column_headers: :obj:`tuple[str]`, default=("ExperimentName", "Subject")
        The initial column headers for data.

    Returns
    -------
    pandas.Dataframe
        A Pandas dataframe of the data.
    """
    with open(log_filepath, "r") as f:
        initial_column_headers = tuple(initial_column_headers)
        textlines = f.readlines()
        delimiter = _determine_delimiter(textlines, initial_column_headers)
        cleaned_textlines = [line for line in textlines if line != "\n"]
        for indx, line in enumerate(cleaned_textlines):
            if line.startswith(f"{delimiter}".join(initial_column_headers)):
                start_indx = indx
                break

        text = "".join(cleaned_textlines[start_indx:])
        df = pd.read_csv(io.StringIO(text, newline=None), sep=delimiter)

        if drop_columns:
            drop_columns = (
                [drop_columns] if isinstance(drop_columns, str) else drop_columns
            )
            df = df.drop(drop_columns, axis=1)

    return (
        df
        if not convert_to_seconds
        else _convert_time(df, convert_to_seconds, divisor=1000)
    )
