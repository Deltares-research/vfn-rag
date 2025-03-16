# voice-for-nature
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Installation
```bash
poetry install
```
### Install only dependencies
```bash
poetry install --no-dev
```
## install dev dependencies
```bash
poetry install --only=dev
```

## install the analysis dependencies
```bash
poetry install --only=analysis
```

to install both the dev and analysis dependencies
```bash
poetry install --only=dev,analysis
```

## Run the Web application
```bash
poetry run streamlit run src\voice_for_nature_backend\app.py
```

# eBird API

## Get API Key
https://ebird.org/api/keygen

## eBird API UI
https://ebird-api-ui.com/


## Help
https://support.ebird.org/en/support/solutions/48000450743?__hstc=75100365.0adbf9eb515854b31ac354f97e0e20b9.1726650992004.1726650992004.1726659709561.2&__hssc=75100365.59.1726659342230&__hsfp=526774486&_gl=1*215rzm*_gcl_au*MTA1MTY0OTY0Ny4xNzI2NjUwOTkx*_ga*MTU5NjA5NTgzMy4xNzI2NjUwOTkx*_ga_QR4NVXZ8BM*MTcyNjY2NDE2Mi4zLjEuMTcyNjY2NDgxOS42MC4wLjA.&_ga=2.32463165.2010216176.1726650991-1596095833.1726650991
