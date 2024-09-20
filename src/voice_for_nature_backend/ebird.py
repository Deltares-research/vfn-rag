from typing import List
from dataclasses import dataclass


@dataclass
class Observation:
    code: str
    common_name: str
    scientific_name: str
    location_id: str
    location_name: str
    observation_date: str
    how_many: int
    latitude: float
    longitude: float
    is_valid: bool
    is_reviewed: bool
    is_private: bool
    sub_id: str


def parse_response(response: dict) -> List[Observation]:
    """Parse the response from the eBird API.

    Parameters
    ----------
    response: [dict]
        The data retrieved from the eBird API.
        >>> [
        >>>     {'speciesCode': 'barwar1',
        >>>     'comName': 'Barred Warbler',
        >>>     'sciName': 'Curruca nisoria',
        >>>     'locId': 'L24992941',
        >>>     'locName': 'Meijendal',
        >>>     'obsDt': '2024-09-15 07:30',
        >>>     'howMany': 1,
        >>>     'lat': 52.1289371,
        >>>     'lng': 4.3332267,
        >>>     'obsValid': False,
        >>>     'obsReviewed': False,
        >>>     'locationPrivate': True,
        >>>     'subId': 'S195328707'}
        >>> ]

    Returns
    -------
    [list]
        A list of Observation objects.

        >>> [
        >>>     Observation(
        >>>             code='barwar1',
        >>>             common_name='Barred Warbler',
        >>>             scientific_name='Curruca nisoria',
        >>>             location_id='L24992941',
        >>>             location_name='Meijendal',
        >>>             observation_date='2024-09-15 07:30',
        >>>             how_many=1,
        >>>             latitude=52.1289371,
        >>>             longitude=4.3332267,
        >>>             is_valid=False,
        >>>             is_reviewed=False,
        >>>             is_private=True,
        >>>             sub_id='S195328707')
        >>> ]

    """
    observations = []
    for items in response:
        observations.append(
            Observation(
                code=items["speciesCode"],
                common_name=items["comName"],
                scientific_name=items["sciName"],
                location_id=items["locId"],
                location_name=items["locName"],
                observation_date=items["obsDt"],
                how_many=items["howMany"],
                latitude=items["lat"],
                longitude=items["lng"],
                is_valid=items["obsValid"],
                is_reviewed=items["obsReviewed"],
                is_private=items["locationPrivate"],
                sub_id=items["subId"],
            )
        )

        return observations
