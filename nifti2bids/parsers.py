from pathlib import Path

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


def _determine_deliminator(textlines: list[str]) -> str | None:
    """
    Identify the deliminator used for the data based on the
    deliminator used for the column titles.

    Parameters
    ----------
    textlines: :obj:`list[str]`
        The lines of text from the presentation log file.

    Returns
    -------
    str or None
        The deliminator or None if the deliminator not determined.
    """
    for line in textlines:
        if line.startswith(PRESENTATION_COLUMNS[0]):
            first_string = line.split(PRESENTATION_COLUMNS[1])[0]
            deliminator = first_string.removeprefix(PRESENTATION_COLUMNS[0])
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


def _convert_time(
    presentation_df: pd.DataFrame, convert_to_seconds: bool
) -> pd.DataFrame:
    """
    Convert timing of the Presentation Dataframe to floats.

    Parameters
    ----------
    presentation_df: :obj:`DataFrame`
        Pandas Dataframe of the Presentation log

    convert_to_seconds: :obj:`bool`, default=False
        Convert resolution of all time columns from 0.1ms to seconds.

    Returns
    -------
    pandas.Dataframe
        Dataframe of Presentation log with timing converted to floats and
        time resolution converted to seconfs if ``convert_to_seconds`` is
        True.
    """
    # Convert timing from strings to floats
    columns = set(["Time", "TTime", "Duration", "ReqTime", "ReqDur"])
    present_columns = list(columns.intersection(presentation_df.columns))
    presentation_df[present_columns] = presentation_df[present_columns].astype(float)

    if convert_to_seconds:
        presentation_df[present_columns] = presentation_df[present_columns].apply(
            lambda x: x / 10000
        )

    return presentation_df


def load_presentation_log(
    log_filepath: str | Path, convert_to_seconds: bool = False
) -> pd.DataFrame:
    """
    Loads Presentation log file as a Pandas Dataframe.

    Parameters
    ----------
    log_filepath: :obj:`str` or :obj:`Path`
        Absolute path to the Presentation log file (i.e text, log, excel files).

    convert_to_seconds: :obj:`bool`, default=False
        Convert resolution of all time columns from 0.1ms to seconds.

    Returns
    -------
    pandas.Dataframe
        A Pandas dataframe of the data.
    """
    with open(log_filepath, "r") as f:
        textlines = f.readlines()
        deliminator = _determine_deliminator(textlines)
        content_indices = []

        cleaned_textlines = [line for line in textlines if line != "\n"]
        for indx, line in enumerate(cleaned_textlines):
            # Get the starting index of the data columns
            if line.startswith(f"{deliminator}".join(PRESENTATION_COLUMNS)):
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

    df = _convert_textlines_to_df(data_textlines, deliminator, PRESENTATION_COLUMNS)

    return _convert_time(df, convert_to_seconds)
