import pandas as pd
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from time import sleep
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from baseball_spider.spider.selenium_manager import create_driver
from baseball_spider.spider.bio import get_player_bio

if TYPE_CHECKING:
    import logging
    from selenium import webdriver


def get_player_abs(  # type: ignore
        player_id_season: str,
        webscrape: bool = True,
        driver: Optional['webdriver'] = None,
        logger: Optional['logging.Logger'] = None,
        ignore_files: bool = False,
        existing_data_folder_path: Optional[str] = None,
        player_bios_path: Optional[str] = None,
        save_folder_path: Optional[str] = None,
        return_data: bool = True,
        ) -> List[Dict[Any, Any]]:
    '''
    Queries baseballsavant.mlb.com for the statcast gamelogs of a given player
    during a given season.

    Args:
        player_id_season: tuple or list of tuples of (player_id, season)
        webscrape: specify whether data should be scraped if necessarygit 
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
    players = []
    if type(player_id_season) is tuple:  # type: ignore
        player_id_season = [player_id_season, ]  # type: ignore
    for player in player_id_season:
        player_id = player[0]
        season = player[1]
        if logger:
            logger.info(
                f'Attemping to retrieve at-bats for {player_id} in {season}.'
                )
        info = get_player_bio(
            player_id=player_id,
            driver=driver,
            webscrape=webscrape,
            filepath=player_bios_path
            )
        if logger:
            logger.info(f'Bio for {info["name"]} retrieved.')

        if not ignore_files and existing_data_folder_path:
            try:
                filepath = (
                    f'{existing_data_folder_path}/{info["player_id"]}_{season}.csv'
                    )
                atbat_dict = pd.read_csv(filepath).to_dict('list')
                if logger:
                    logger.info(
                        f'Existing data for {info["name"]} found for {season}.'
                        )
                if save_folder_path:
                    save_at_bats(
                        atbat_dict,
                        save_folder_path+f'/{player_id}_{season}.csv'
                        )
                if return_data:
                    players.append(atbat_dict)
                continue
            except FileNotFoundError as e:
                if logger:
                    logger.info(
                        f'No existing data for {info["name"]} found for {season}.'
                        )
                if not webscrape:
                    raise FileNotFoundError(e)
        atbat_dict = {
            'player_id': [],
            'date': [],
            'opponent': [],
            'result': [],
            'ev': [],
            'la': [],
            'distance': [],
            'direction': [],
            'pitch_velo': [],
            'pitch_type': [],
            }
        if not driver:
            driver = create_driver()
        if info['position'] == 'P':
            gamelog_type = 'pitching'
        else:
            gamelog_type = 'hitting'
        atbat_url = (
            f'https://baseballsavant.mlb.com/savant-player/{player_id}?'
            f'stats=gamelogs-r-{gamelog_type}-statcast&season={season}'
                    )
        # attempts to scrape the data 5 times until failing
        data_scraped = False
        scrape_attempts = 0
        while not data_scraped:
            scrape_attempts += 1
            try:
                driver.get(atbat_url)
            except InvalidSessionIdException:
                driver = create_driver()
                driver.get(atbat_url)
            atbat_table = driver.find_element_by_id('gamelogs_statcast')
            table_rows = atbat_table.find_elements_by_class_name('default-table-row')
            if len(table_rows) > 0:
                data_scraped = True
            elif scrape_attempts >= 5:
                raise TimeoutException(
                    'Data could not be scraped after 5 attempts. Check to ensure'
                    'the url and element information is correct and try again.'
                    )
            else:
                sleep(5)
        for row in table_rows:
            atbat_dict['player_id'].append(info['player_id'])
            atbat_dict['date'].append(row.find_element_by_xpath('td[2]').text)
            atbat_dict['opponent'].append(row.find_element_by_xpath('td[5]').text)
            atbat_dict['result'].append(row.find_element_by_xpath('td[6]').text)
            atbat_dict['ev'].append(row.find_element_by_xpath('td[7]').text)
            atbat_dict['la'].append(row.find_element_by_xpath('td[8]').text)
            atbat_dict['distance'].append(row.find_element_by_xpath('td[9]').text)
            atbat_dict['direction'].append(row.find_element_by_xpath('td[10]').text)
            atbat_dict['pitch_velo'].append(row.find_element_by_xpath('td[11]').text)
            atbat_dict['pitch_type'].append(row.find_element_by_xpath('td[12]').text)

        if len(atbat_dict['player_id']) < 1 and logger:
            logger.info(f'No at-bats for {player_id} in {season}.')
        elif logger:
            logger.info(f'At-bats for {info["name"]} in {season} retrieved.')

        if save_folder_path:
            save_at_bats(atbat_dict, save_folder_path+f'/{player_id}_{season}.csv')
        if return_data:
            players.append(atbat_dict)

    if return_data:
        return players


def save_at_bats(at_bats: Dict[Any, Any], filepath: str):
    '''
    Saves at bat data to specified filepath.

    args:
        at_bats: dictionary of at bat data
        filepath: filepath the data will be saved to
    '''
    if len(at_bats['player_id']) < 1:
        raise ValueError('The at bat dictionary is empty. Data cannot be saved.')
    pd.DataFrame(at_bats).to_csv(filepath, index=False)
