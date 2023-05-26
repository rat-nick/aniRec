import pandas as pd


def extract_itemID(url: pd.Series) -> pd.Series:
    """Extracts itemID from the URL

    Parameters
    ----------
    url : pd.Series
        The series containing URLs

    Returns
    -------
    pd.Series
        The series containing itemIDs
    """
    return url.str.split("/").str.get(-2)
