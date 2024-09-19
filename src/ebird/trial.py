import os
import requests

BASE_URL = "https://api.ebird.org/v2"
DATA_OBS_URL = f"{BASE_URL}/data/obs"
# Set your eBird API key here
API_KEY = os.environ["API_KEY"]

region_code = "NL-ZH"
lat = 51.9865
lon = 4.3815
location = f"?lat={lat}&lng={lon}"

# The eBird species code.
species_code = "baleag1"

# date
year = 2021  # from 1800 to present
month = 10
day = 1
date = f"{year}/{month}/{day}"
# %% Recent observations in a region
# Set the base URL for the eBird API
# Recent observations of a species in a region
url = f"{DATA_OBS_URL}/{region_code}/recent"
# Recent notable observations in a region
url = f"{DATA_OBS_URL}/{region_code}/recent/notable"
# Recent observations of a species in a region
url = f"{DATA_OBS_URL}/{region_code}/recent/{species_code}"
# Recent nearby observations
url = f"{DATA_OBS_URL}/geo/recent{location}"
# Nearest observations of a species
url = f"{BASE_URL}/data/nearest/geo/recent/{species_code}{location}"
# Recent nearby notable observations
url = f"{DATA_OBS_URL}/geo/recent/notable{location}"
# Historic observations on a date
url = f"{DATA_OBS_URL}/{species_code}/historic/{date}"
# Top 100
url = f"{BASE_URL}/product/top100/{species_code}/{date}"
# Recent checklists feed
url = f"{BASE_URL}/product/lists/{region_code}"
# Checklist feed on a date
url = f"{BASE_URL}/product/lists/{region_code}/{date}"
# Regional statistics on a date
url = f"{BASE_URL}/product/stats/{region_code}/{date}"
# Species List for a Region
url = f"{BASE_URL}/product/spplist/{region_code}"
# View Checklist
url = f"{BASE_URL}/product/checklist/view/{{subId}}"


# %%
# Set up the headers with your API key
headers = {"x-ebirdapitoken": API_KEY}

# Make a GET request to the eBird API to get recent bird observations in the region
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Print the retrieved data
    for observation in data:
        print(
            f"Species: {observation['comName']}, Location: {observation['locName']}, Date: {observation['obsDt']}"
        )
else:
    # Print error message if the request failed
    print(f"Error: Unable to fetch data (status code {response.status_code})")
