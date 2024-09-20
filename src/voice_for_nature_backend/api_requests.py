from typing import Dict, Union
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)


def make_request(url: str, headers: Dict[str, str]) -> Union[Dict[str, str], None]:
    """Make a GET request to the eBird API and print the results.

    Parameters
    ----------
    url: [str]
        The URL of the API endpoint to request.
    headers: [dict]
        The headers to include in the request.

    Returns
    -------
    [dict]
        The data retrieved from the eBird API.
    """
    # Make a GET request to the eBird API to get recent bird observations in the region
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        return data
    else:
        # Print error message if the request failed
        logging.error(
            f"Error: Unable to fetch data (status code {response.status_code})"
        )
