# Baseball Spider
This is a library to easily "query" player data from [Baseball Savant](https://www.baseballsavant.com) and [MLB.com](https://www.mlb.com). The library scrapes data using Selenium and returns it as a dictionary.

# Functions
These are the currently available functions to call that return data. This list and the individual details within will be expanded as new functionality are incorporated into the library.

## `id.get_mlb_ids()`

## `bio.get_bios()`

## `stats.get_stats()`

# Notes on running
If you plan to install or clone this library, there are a couple things to note about the web scraping process, that you may need to alter to accomodate your environment.

- This library currently uses [webdriver_manager](https://pypi.org/project/webdriver-manager/) to get a webdriver that Selenium can use to access sites. In the future it will be able to use most web browsers, but it is currently only set to use Chrome webdrivers. So for this library to run, you will need a Chromium based browser installed in your environment.
- In addition, you will need to ensure that your browser version aligns with the webdriver version that is downloaded (currently `109.0.5414.74`). In the future, the library will dynamically select the most appropriate version, if one is available. If you wish to use an alternate version, change the version in `create_driver()` within `selenium_manager.py`.

## Examples
