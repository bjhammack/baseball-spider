from datetime import datetime as dt
from os.path import exists, isdir, join
from os import mkdir
import pandas as pd
from selenium_manager import create_driver
import traceback
from typing import Optional

from player_ids import get_current_ids
from bio import get_player_bio, get_all_bios


def gather_all_at_bats(parent_path: str):
    '''
    Gets all player bios, then loops through players, pulling all their seasons.
    Saves data in sub directories sorted by season (function will create sub
    folders for each position and store players there if they do not exist).

    args:
        parent_path: path to folder all players will be under (must have '/' at
                     the end)
    '''
    driver, logger = create_driver()
    positions = ['1B','2B','3B','SS','OF','C','P']
    if not isdir(parent_path):
        raise Exception('Parent path does not exist. Specify an existing path.')
    for position in positions:
        full_path = join(parent_path, position)
        if not isdir(full_path):
            mkdir(full_path)
            logger.info(f'Created path {full_path}.')
        else:
            logger.info(f'Using existing path {full_path}.')
    bios_df = get_all_bios(driver, logger)
    failed = []
    seasons = list(range(2015,dt.now().year+1))
    for k,v in bios_df.iterrows():    
        for season in seasons:
            try:
                atbat_dict = get_at_bats(v["player_id"], season, driver, logger)
                if len(atbat_dict['player_id']) < 1:
                    continue
                df = pd.DataFrame(atbat_dict)
                save_filepath = f'{parent_path}{v["position"]}/{v["player_id"]}_{season}.csv'
                save_at_bats(atbat_dict, save_filepath)
            except:
                error = traceback.format_exc()
                logger.error(f'Error during {v["player_id"]}-{season} retrieval: {error}')
                print(f'{v["player_id"]} - {season} failed.')
                failed.append(f'{v["player_id"]} - {season}')


def get_at_bats(
    player_id: str,
    season: int,
    driver: Optional['selenium.webdriver.chrome.webdriver.WebDriver'] = None,
    logger: Optional['logging.Logger'] = None,
    ignore_files: bool = False,
    save: bool = False,
    save_filepath: Optional[str] = None,
    ) -> dict:
    '''
    Queries baseballsavant.mlb.com for the statcast gamelogs of a given player
    during a given season.

    Args:
        player_id: mlb.com player ID for the target player
        season: target season in range 2015 - current year
        driver: selenium webdriver being used to connect to the website
        logger: python logger for backtracing
        ignore_files: ignores if a CSV already exists and scrapes the data
        save: Saves data to file if true
        save_filepath: path to save data to if save 

    Returns:
        atbat_dict: Dictionary of at bats scraped
    '''
    logger.info(f'Attemping to retrieve at-bats for {player_id} in {season}.')
    atbat_dict = {
        'player_id':[],
        'date':[],
        'opponent':[],
        'result':[],
        'ev':[],
        'la':[],
        'distance':[],
        'direction':[],
        'pitch_velo':[],
        'pitch_type':[],
        }
    info = get_player_bio(player_id, driver)
    logger.info(f'Bio for {info["name"]} retrieved.')

    potential_filepath = f'data/at_bats/{info["position"]}/{info["player_id"]}_{season}.csv'
    if exists(potential_filepath) and not ignore_files:
        logger.info(f'Existing data for {info["name"]} found for {season}.')
        return pd.read_csv(potential_filepath).to_dict()
        
    if info['position'] == 'P':
        gamelog_type = 'pitching'
    else:
        gamelog_type = 'hitting'
    atbat_url = f'https://baseballsavant.mlb.com/savant-player/{player_id}?stats=gamelogs-r-{gamelog_type}-statcast&season={season}'
    driver.get(atbat_url)
    atbat_table = driver.find_element_by_id('gamelogs_statcast')
    table_rows = atbat_table.find_elements_by_class_name('default-table-row')
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

    if len(atbat_dict['player_id']) < 1:
        logger.info(f'No at-bats for {player_id} in {season}.')
    else:
        logger.info(f'At-bats for {info["name"]} in {season} retrieved.')

    if save:
        save_at_bats(atbat_dict, save_filepath)

    return atbat_dict


def save_at_bats(at_bats: dict, filepath: str):
    if len(at_bats['player_id']) < 1:
        print('The dictionary is empty. Aborting...')
        return
    pd.DataFrame(at_bats).to_csv(filepath)