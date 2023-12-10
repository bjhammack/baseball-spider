# Baseball Spider
This is a library to easily "query" player data from [Baseball Savant](https://www.baseballsavant.com) and [MLB.com](https://www.mlb.com). The library scrapes data using Selenium and returns it as a dictionary.

# Functions
These are the currently available functions to call that return data. This list and the individual details within will be expanded as new functionality are incorporated into the library.

## `id.get_mlb_ids()`
Gathers all available IDs from mlb.com, going through its index of players and pulling their IDs from the metadata and returns them as a dictionary.

### Arguments
- `return_data`: bool - Specifies if the function should return the data.
- `save_path`: str - If provided, the dictionary will be written to this path as a CSV. If not provided, no data will be saved.
- `driver`: webdriver - The selenium webdriver to be used for the webscraping. If none provided, one will be created.

### Returns
- `id_dict`: dict - A dictionary with a single key (player_id) that contains all the IDs scraped from mlb.com.

## `bio.get_bios()`
Gathers biographical information about a specified player from Baseball Savant.

### Arguments
- `player_id`: str|list - player_id or list of player_ids to get biographical information for.
- `return_data`: bool - Specifies if the function should return the data.
- `save_path`: str - If provided, the dictionary will be written to this path as a CSV. If not provided, no data will be saved.
- `driver`: webdriver - The selenium webdriver to be used for the webscraping. If none provided, one will be created.

### Returns
- `bio_dict`: dict - A dictionary of player biographical data, with the below keys:
    - player_id
    - name
    - position (options: SP, RP, C, 1B, 2B, 3B, SS, OF, DH)
    - b/t (the handedness of a player, eg. R/R)
    - age

## `stats.get_stats()`
Gathers a variety of stats, based on user input, from Baseball Savant.

### Arguments
- `player_id`: str|list - player_id or list of player_ids to get biographical information for.
- `stat_type`: str - The type of stats to be scraped.
- `return_data`: bool - Specifies if the function should return the data.
- `save_path`: str - If provided, the dictionary will be written to this path as a CSV. If not provided, no data will be saved.
- `driver`: webdriver - The selenium webdriver to be used for the webscraping. If none provided, one will be created.

#### Stat Type
As noted in the arguments, `stat_type` allows the user to specify which stats are gathered from Baseball Savant. Below are the current options are which stats are gathered by them.
| statcast_running | statcast_season | statcast_at_bat | standard_game | standard_season |
|------------------|-----------------|-----------------|---------------|-----------------|
| player_id        | player_id       | player_id       | player_id     | player_id       |
| season           | season          | date            | date          | season          |
| ft/s             | pitches         | opponent        | home          | g               |
| hp-1st           | balls           | result          | away          | pa              |
| bolts            | barrels         | ev              | pa            | ab              |
| pos_rank         | barrel%         | la              | ab            | r               |
| age_rank         | barrel/pa       | distance        | r             | h               |
| league_rank      | ev              | direction       | h             | 2B              |
| percentile       | max_ev          | pitch_velo      | 2B            | 3B              |
|                  | la              | pitch_type      | 3B            | hr              |
|                  | sweet_spot%     |                 | hr            | rbi             |
|                  | xba             |                 | rbi           | bb              |
|                  | xslg            |                 | bb            | k               |
|                  | woba            |                 | k             | sb              |
|                  | xwoba           |                 | sb            | cs              |
|                  | xwobacon        |                 | cs            | hbp             |
|                  | hh%             |                 | hbp           | avg             |
|                  | k%              |                 | avg           | obp             |
|                  | bb%             |                 | obp           | slg             |
|                  |                 |                 | slg           |                 |

### Returns
- `players`: list[dict] - A list of dictionaries that contain keys of one of the above table columns, depending on which stat_type was used.


# Notes on running
If you plan to install or clone this library, there are a couple things to note about the web scraping process, that you may need to alter to accomodate your environment.

- This library currently uses [webdriver_manager](https://pypi.org/project/webdriver-manager/) to get a webdriver that Selenium can use to access sites. In the future it will be able to use most web browsers, but it is currently only set to use Chrome webdrivers. So for this library to run, you will need a Chromium based browser installed in your environment.
- In addition, you will need to ensure that your browser version aligns with the webdriver version that is downloaded (currently `109.0.5414.74`). In the future, the library will dynamically select the most appropriate version, if one is available. If you wish to use an alternate version, change the version in `create_driver()` within `selenium_manager.py`.
