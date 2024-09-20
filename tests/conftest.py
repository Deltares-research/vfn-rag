from typing import Dict, List
import pytest


@pytest.fixture
def ebird_response() -> List[Dict[str, str]]:
    return [
        {
            "speciesCode": "barwar1",
            "comName": "Barred Warbler",
            "sciName": "Curruca nisoria",
            "locId": "L24992941",
            "locName": "Meijendal",
            "obsDt": "2024-09-15 07:30",
            "howMany": 1,
            "lat": 52.1289371,
            "lng": 4.3332267,
            "obsValid": False,
            "obsReviewed": False,
            "locationPrivate": True,
            "subId": "S195328707",
        }
    ]
