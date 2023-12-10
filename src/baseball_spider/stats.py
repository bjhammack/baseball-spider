from elements import get_vars
import pandas as pd
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from selenium.webdriver.common.by import By
from time import sleep
from tqdm import tqdm
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
        player_id: mlb.com player ID for given player
        stat_type: type of stats to scrape
        return_data: bool to determine if anything will be returned
        save_path: path to save as CSV, if none, stats will not be saved
        driver: selenium webdriver being used to connect to the website

    Returns:
        players: optional list of dictionaries of stats scraped
    '''
    season = None
    players = []
    failed_players = []
    if type(player_id) in (str, tuple):
        player_id = [player_id, ]
    pbar = tqdm(player_id)
    for player in pbar:
        pbar.set_description(
            f'Current: {player if type(player) is str else player[0]}; '
            f'Failures: {len(failed_players)}'
            )
        if type(player) is tuple:
            season = player[1]
            player = player[0]
        vars = get_vars(stat_type, player, season)
        stats_dict = {k: [] for k in vars['keys']}

        if not driver:
            driver = create_driver()
        # attempts to scrape the data 5 times until failing
        failed = False
        scraped = False
        attempts = 0
        while not scraped:
            attempts += 1
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
                        By.CLASS_NAME, 'th-component-header'
                        )[vars['test_header_index']].text
                    if test_header == vars['test_header']:
                        table_rows = table.find_elements(
                            By.CLASS_NAME, 'default-table-row')
                        break
                except:
                    if i+1 == len(tables):
                        if len(player_id) == 1:
                            raise ValueError(f'Unable to find table with correct '
                                f'headers after checking {len(tables)} tables.')
                        scraped = True
                        failed = True
                    pass

            if len(table_rows) > 0:
                scraped = True
            elif attempts >= 5:
                exc_text = f'Could not find {player} stats after 5 attempts.'
                if len(player_id) == 1:
                    raise TimeoutException(exc_text)
                scraped = True
                failed = True
            else:
                sleep(5)
        if failed:
            failed_players.append(player)
            continue
        
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

    print(f'{len(failed_players)} players unable to be scraped.\n{failed_players}')
    if return_data:
        return players


def save_data(players: Dict[Any, Any], expected_keys, filepath: str):
    '''
    Saves at bat data to specified filepath.

    args:
        players: dictionary containing data
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
