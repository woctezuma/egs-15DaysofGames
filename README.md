# EGS: 15 Days of Games

[![Build status with Github Action][build-image-action]][build-action]
[![Code coverage][codecov-image]][codecov]
[![Code Quality][codacy-image]][codacy]

This repository contains Python code to data-mine the 15 Days of (free) Games at the Epic Games Store (EGS).

## Requirements

-   Install the latest version of [Python 3.X][python-download-url].
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To download data of upcoming promotions:

```bash
python download_data.py
```

To filter promotions to focus on potential free games:

```bash
python filter_promotions.py
```

## References

API documentation:

- [`SD4RK/epicstore_api`][egs-api-python]: a Python wrapper for the EGS API,
- [`Tectors/EpicGraphql`][egs-api-graphql]: a documentation of GraphQL queries for the EGS API,

Data leaks:

-   [`egs-datamining`][egs-datamining]: datamining of Epic Games Store (EGS),
-   [`geforce-leak`][geforce-leak]: datamining of Nvidia's GeForce NOW (GFN),



<!-- Definitions -->

[build-action]: <https://github.com/woctezuma/egs-15DaysofGames/actions>
[build-image-action]: <https://github.com/woctezuma/egs-15DaysofGames/workflows/Python application/badge.svg?branch=main>

[codecov]: <https://codecov.io/gh/woctezuma/egs-15DaysofGames>
[codecov-image]: <https://codecov.io/gh/woctezuma/egs-15DaysofGames/branch/main/graph/badge.svg>

[codacy]: <https://www.codacy.com/gh/woctezuma/egs-15DaysofGames>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/3c06156df0dc4e26956e1dd9c17cb57b>

[python-download-url]: <https://www.python.org/downloads/>

[egs-api-python]: <https://github.com/SD4RK/epicstore_api>
[egs-api-graphql]: <https://github.com/Tectors/EpicGraphql>

[egs-datamining]: <https://github.com/woctezuma/egs-datamining>
[geforce-leak]: <https://github.com/woctezuma/geforce-leak>
