from typing import List, Dict
from voice_for_nature_backend.ebird import Observation, parse_response


def test_parse_response(ebird_response: List[Dict[str, str]]):
    parsed_response = parse_response(ebird_response)
    assert isinstance(parsed_response, List)
    assert all(isinstance(obs, Observation) for obs in parsed_response)
