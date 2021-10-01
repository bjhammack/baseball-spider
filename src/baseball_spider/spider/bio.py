import pandas as pd
from typing import Optional, Dict, Any, Sequence, Type

from baseball_spider.spider.player_ids import _get_current_ids
from baseball_spider.spider.selenium_manager import create_driver


def get_player_bio(
    player_id: str,
    parent_data_dir: Optional[str] = None,
    webscrape: bool = True,
    driver: Optional['selenium.webdriver'] = None, # type: ignore
    ) -> Dict[str, str]:
    '''
    Queries baseballsavant.mlb.com to get biographical information on a player.

    args:
        player_id: mlb.com player ID for given player
        parent_data_dir: parent folder for all locally stored data
        webscrape: if webscrape, then create a driver if one is not provided
                   for scraping
        driver: selenium webdriver being used to connect to the website

    returns:
        info_dict: dictionary of player info
    '''
    try:
        if not parent_data_dir:
            raise Exception('No local data specified.')
        info_df = pd.read_csv(f'{parent_data_dir}/player_bios.csv')
        info_dict = info_df.loc[info_df.player_id.eq(player_id)].to_dict('records')[0]
        if len(info_dict['player_id']) > 1:
            return info_dict
    except:
        print('player_bios.csv either does not exist or player is not in it.')
    if not webscrape:
        raise Exception('No existing data found and no driver provided for scraping.')
    if not driver:
        driver = create_driver()
    info_dict = {}
    url = f'https://baseballsavant.mlb.com/savant-player/{player_id}'
    driver.get(url)
    info_div = driver.find_element_by_class_name('bio-player-name')
    info_dict['name'] = info_div.find_element_by_xpath('div[1]').text
    details_row = info_div.find_element_by_xpath('div[2]').text
    info_dict['position'] = details_row.split()[0]
    if info_dict['position'] in ('LF','RF','CF'):
        info_dict['position'] = 'OF'
    info_dict['player_id'] = player_id
    driver.close()

    return info_dict


def get_all_bios(
    parent_data_dir: Optional[str] = None,
    webscrape: bool = True,
    driver: Optional['selenium.webdriver'] = None, # type: ignore
    save_data_filepath: Optional[str] = None,
    logger: Optional['logging.Logger'] = None # type: ignore
    ) -> Sequence[Type[Dict[Any, Any]]]:
    '''
    Gets all bios from exisiting bios file or pulls bios from web if file DNE.

    args:
        parent_data_dir: parent folder for all locally stored data
        driver: optional selenium webdriver if bios need to be scraped
        save_data_filepath: if specified, location to save data as a CSV. If none,
                            data will not be saved.
        logger: logger to track webscraping

    returns:
        list of dictionaries of all player bios
    '''
    try:
        if not parent_data_dir:
            raise Exception('No local data specified.')
        bios_df = pd.read_csv(f'{parent_data_dir}/player_bios.csv')
        return bios_df.to_dict('records')
    except:
        print('player_bios.csv either does not exist or player is not in it.')
    if not webscrape:
        raise Exception('No existing data found and no driver provided for scraping.')
    if not driver:
        driver = create_driver()
    ids = _get_current_ids(parent_data_dir=parent_data_dir, driver=driver)
    all_players = [dict]
    for player_id in ids.player_id:
        player_bio = get_player_bio(player_id, driver)
        if logger:
            logger.info(f'Bio for {player_bio["name"]} gathered.')
        all_players.append(player_bio) # type: ignore
    if save_data_filepath:
        bios_df = pd.DataFrame(all_players)
        bios_df.to_csv(f'{save_data_filepath}', index=False)
    driver.close()

    return all_players