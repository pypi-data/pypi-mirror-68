from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def generate_dates(year: int) -> List[date]:
    """[Generates a list of all the week beginings in year. Note: Weeks start on Sundays]

    Arguments:
        year {int} -- [The year to generate a list of dates for]

    Returns:
        List[str] -- [List of str representations of datetime.date objects for the year]
    """
    dates = []
    d = date(year, 1, 1)  # January 1st
    d += timedelta(days=6 - d.weekday())  # First Sunday
    while d.year == year:
        dates.append(d)
        d += timedelta(days=7)
        if d.year != year:
            break
    return dates


def dict_rename(data: Dict[str, Any], rename: Dict[str, Any]) -> Dict[str, Any]:
    for original, new in rename.items():
        data[new] = data[original]
        data.pop(original)

    return data


def read_arl(filename: str) -> str:
    with open(filename) as file:
        arl = file.readlines()[0].strip()
        return arl


def read_acoustid(filename: str) -> str:
    with open(filename) as file:
        key = file.readlines()[0].strip()
        return key


def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 0.3,
    status_forcelist: Tuple[int, int, int] = (500, 502, 504),
    session: Optional[requests.Session] = None,
) -> requests.Session:
    session = session or requests.Session()
    retry = Retry(
        total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def sort_title(text: str) -> str:
    text.lstrip("A ").lstrip("The ")

    return text


def url_to_deezer_id(url: str) -> str:
    return url.split("/")[-1]


def replace_illegals(text: str) -> str:
    text.replace("/", "_")
    return text
