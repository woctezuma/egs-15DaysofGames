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

### Work-In-Progress

(Optional) To receive a temporary authorization code:

```bash
python check_auth.py
```

NB: cookie information is required to be able to receive a temporary authorization code from within Python.

<details><summary>How to fill-in your cookie information</summary>
1. Make sure you are connected to your [Epic Games][epic-games-store-login] account,
2. Press `<Shift-F9>` in your web browser to access the storage section of the developer tools,
3. Use the filtering option to find the cookie value for `EPIC_SESSION_AP`, 
4. Copy-paste this cookie value into a new file called `data/personal_info.json`:
   ```json
   {
       "EPIC_SESSION_AP": "PASTE_YOUR_COOKIE_VALUE_HERE"
   }  
   ```
</details>

## Results

Results are shown [on the Wiki][wiki-results].

A retrospective analysis of the results is conducted [on the homepage of the Wiki][wiki-retrospective-look].

An investigation of the leaks found online is conducted [on the Investigation page of the Wiki][wiki-investigation].

## References

API documentation:

-   [`SD4RK/epicstore_api`][egs-api-python]: a Python wrapper for the EGS API,
-   [`Tectors/EpicGraphql`][egs-api-graphql]: a documentation of GraphQL queries for the EGS API,
-   [`MixV2/EpicResearch`][egs-api-clients]: a documentation of Auth Clients' name, id and secret,
-   [`derrod/legendary`][egs-api-hosts]: a documentation of API hosts, along with access token management in [`api/egs.py`][egs-api-token],
-   [`acidicoala/ScreamDB`][egs-web-app]: a web app to view EGS item ids,

Data leaks:

-   [`egs-datamining`][egs-datamining]: datamining of Epic Games Store (EGS),
-   [`geforce-leak`][geforce-leak]: datamining of Nvidia's GeForce NOW (GFN),

GraphQL advice:

-   A few [pieces of advice][wiki-graphQL] regarding GraphQL.

<!-- Definitions -->

[build-action]: <https://github.com/woctezuma/egs-15DaysofGames/actions>
[build-image-action]: <https://github.com/woctezuma/egs-15DaysofGames/workflows/Python application/badge.svg?branch=main>

[codecov]: <https://codecov.io/gh/woctezuma/egs-15DaysofGames>
[codecov-image]: <https://codecov.io/gh/woctezuma/egs-15DaysofGames/branch/main/graph/badge.svg>

[codacy]: <https://www.codacy.com/gh/woctezuma/egs-15DaysofGames>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/3c06156df0dc4e26956e1dd9c17cb57b>

[python-download-url]: <https://www.python.org/downloads/>
[epic-games-store-login]: <https://www.epicgames.com/login>

[wiki-results]: <https://github.com/woctezuma/egs-15DaysofGames/wiki/Upcoming-Promotions>
[wiki-graphql]: <https://github.com/woctezuma/egs-15DaysofGames/wiki/GraphQL>
[wiki-retrospective-look]: <https://github.com/woctezuma/egs-15DaysofGames/wiki>
[wiki-investigation]: <https://github.com/woctezuma/egs-15DaysofGames/wiki/Investigation>

[egs-api-python]: <https://github.com/SD4RK/epicstore_api>
[egs-api-graphql]: <https://github.com/ToutinRoger/FortniteFovChanger>
[egs-api-clients]: <https://github.com/MixV2/EpicResearch>
[egs-api-hosts]: <https://github.com/derrod/legendary>
[egs-api-token]: <https://github.com/derrod/legendary/blob/master/legendary/api/egs.py>
[egs-web-app]: <https://github.com/acidicoala/ScreamDB>

[egs-datamining]: <https://github.com/woctezuma/egs-datamining>
[geforce-leak]: <https://github.com/woctezuma/geforce-leak>
