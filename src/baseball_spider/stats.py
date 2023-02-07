from elements import get_vars
import pandas as pd
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from selenium.webdriver.common.by import By
from time import sleep
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from selenium_manager import create_driver

if TYPE_CHECKING:
    import logging
    from selenium import webdriver


def get_stats(  # type: ignore
        player_id: List[str] | str,
        stat_type: str,
        return_data: bool = True,
        save_path: Optional[str] = None,
        driver: Optional['webdriver'] = None,
        ) -> List[Dict[Any, Any]]:
    '''
    Queries baseballsavant.mlb.com for the statcast running of a given player
    during a given season.

    Args:
        player_id_season: tuple or list of tuples of (player_id, season)
        webscrape: specify whether data should be scraped if necessary
        driver: selenium webdriver being used to connect to the website
        logger: python logger for backtracing
        ignore_files: ignores if a CSV already exists and scrapes the data
        existing_data_folder_path: path to folder containing existing player data
        player_bios_path: path to player_bios.csv, if exists
        save_folder_path: path to folder to save data
        return_data: bool to determine if anything will be returned

    Returns:
        atbat_dict: optional list of dictionaries of at bats scraped
    '''
    season = None
    players = []
    if type(player_id) in (str, tuple):
        player_id = [player_id, ]
    for player in player_id:
        if type(player) is tuple:
            season = player[1]
            player = player[0]
        vars = get_vars(stat_type, player, season)
        stats_dict = {k: [] for k in vars['keys']}

        if not driver:
            driver = create_driver()
        # attempts to scrape the data 5 times until failing
        data_scraped = False
        scrape_attempts = 0
        while not data_scraped:
            scrape_attempts += 1
            try:
                driver.get(vars['url'])
            except InvalidSessionIdException:
                driver = create_driver()
                driver.get(vars['url'])

            tables = driver.find_elements(By.CLASS_NAME, 'table-savant')
            table_rows = []
            for i, table in enumerate(tables):
                try:
                    table_headers = table.find_elements(
                        By.CLASS_NAME, 'tr-component-row')
                    test_header = table_headers[0].find_elements(
                        By.CLASS_NAME, 'th-component-header'#'tablesorter-header-inner'
                        )[vars['test_header_index']].text
                    if test_header == vars['test_header']:
                        table_rows = table.find_elements(
                            By.CLASS_NAME, 'default-table-row')
                        break
                except:
                    if i+1 == len(tables):
                        raise ValueError(f'Unable to find table with correct '
                            f'headers after checking {len(tables)} tables.')
                    pass

            if len(table_rows) > 0:
                data_scraped = True
            elif scrape_attempts >= 5:
                exception_text = (
                    f'Data could not be found for {player} after 5 attempts. '
                    'Ensure the url and element information are correct and '
                    'try again.')
                if len(player_id) > 1:
                    print(f'{exception_text} Processing other players...')
                    data_scraped = True
                    continue
                else:
                    raise TimeoutException(exception_text)
            else:
                sleep(5)
        
        keys = list(stats_dict.keys())
        for row in table_rows:
            if 'footer-class' in row.get_attribute('class'):
                break
            elif ('static' in row.get_attribute('class') or
                'aggregate-row' in row.get_attribute('class')):
                continue
            stats_dict['player_id'].append(player)
            for i in range(1, len(keys)):
                stats_dict[keys[i]].append(
                    row.find_element(By.XPATH, vars['elements'][i-1]).text)

        players.append(stats_dict)
    
    driver.close()
    if save_path:
        save_data(players, vars['keys'], save_path,)

    if return_data:
        return players


def save_data(players: Dict[Any, Any], expected_keys, filepath: str):
    '''
    Saves at bat data to specified filepath.

    args:
        at_bats: dictionary of at bat data
        filepath: filepath the data will be saved to
    '''
    actual_keys = list(players[0].keys())
    expected_keys.sort()
    actual_keys.sort()
    if len(actual_keys) == 0 or expected_keys != actual_keys:
        raise ValueError(
            f'Expected dictionary with keys: {expected_keys}.'
            f'Got: {tuple(players[0].keys())}'
            )
    if len(players) < 1:
        raise ValueError('The player list is empty. Data cannot be saved.')
    dfs = [pd.DataFrame(player) for player in players]
    data = pd.concat(dfs, ignore_index=True)
    data.to_csv(filepath, index=False)
