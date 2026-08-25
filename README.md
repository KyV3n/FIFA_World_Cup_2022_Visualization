# FIFA World Cup 2022 Visualization

This repository contains code for visualization of the FIFA World Cup 2022 with a focus on how age correlates with performance.
The visualization is made through Dash. The repository also contains scripts for cleaning and exploring the raw data.

## Overview
- [Scripts](#scripts)
- [Usage](#usage)
- [Data](#data)
- [Dependencies](#dependencies)

## Scripts
The `workbooks` directory contains various files to obtain and clean data
- `all_data.py` loads all data from `Data`.
- `create_defence_data.py` uses various data files to create a single .csv file (`defense.csv`) specifically for players in the defender role. This also includes some additional data exploration.
- `rating_SofaScore_data.py` obtains player rating data from SofaScore and puts this into `ratings.csv`. Additionally, it merges this player rating data with an existing raw file to create `player_stats_rating.csv` for further use on the Dash home page.

The resulting .csv files get places directly into the `data` directory for use in the Dash visualization.

## Data
All the raw data is freely available on kaggle:
- FIFA World Cup 2022 [Player Data](https://www.kaggle.com/datasets/swaptr/fifa-world-cup-2022-player-data)
- FIFA World Cup 2022 [Match Data](https://www.kaggle.com/datasets/swaptr/fifa-world-cup-2022-match-data)
- FIFA World Cup 2022 [Team Data](https://www.kaggle.com/datasets/swaptr/fifa-world-cup-2022-statistics)
- FIFA World Cup 2022 [Twitter Data](https://www.kaggle.com/datasets/kumari2000/fifa-world-cup-twitter-dataset-2022)
- FIFA World Cup 2022 [Prediction](https://www.kaggle.com/datasets/shilongzhuang/soccer-world-cup-challenge)
- FIFA World Cup 2022 [Player Images](https://www.kaggle.com/datasets/soumendraprasad/fifa-2022-all-players-image-dataset)
- FIFA World Cup [Historic Data](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup)
- FIFA World Cup [Penalty](https://www.kaggle.com/datasets/pablollanderos33/world-cup-penalty-shootouts) [Shootouts](https://www.kaggle.com/datasets/jandimovski/world-cup-penalty-shootouts-2022)

Not all this raw data is used throughout the current project, but can be found under `workbooks/Data`.

This raw data is used to create cleaned versions in `workbooks`.

`defense_dictionary.csv` is obtained by manually parsing through and selecting the relevant attributes from `workbooks/Data/FIFA World Cup 2022 Player Data/player_data_description.json`.

Additionally, player rating from SofaScore in .json format is obtained through a web URL request.

## Usage
To run the project, run `app.py` to launch the Dash webapp.

## Dependencies
The packages that are used throughout all files:

```
pandas~=3.0.5
plotly~=6.9.0
matplotlib~=3.11.1
numpy~=2.5.2
pillow~=12.3.0
curl_cffi~=0.16.1
seaborn~=0.13.2
tabulate~=0.10.0
dash-bootstrap-components~=2.0.4
dash~=4.4.1
statsmodels~=0.14.6
dash_daq~=0.6.0
natsort~=8.4.0
scikit-learn~=1.9.0
requests~=2.34.2
```
