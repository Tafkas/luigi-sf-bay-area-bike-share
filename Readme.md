# Luigi San Francisco Data Pipeline

This repository contains code to import the anonymized bike trip data from August 2013 to August 2015 provided by [Kaggle](https://www.kaggle.com).


## Getting Started

- Download the data from the [Kaggle website](https://www.kaggle.com/benhamner/sf-bay-area-bike-share/data) and put into `data`.
- Install Python dependencies with Pipenv: `pipenv install Pipfile.lock`
- Create the Postgres Database with `make create-postgres-db`
- Run the luigi daemon with `luigid`
- Run the pipeline with `python import_sfbike.py`
