import pandas as pd
from typing import Optional

from baseball_spider.spider.player_ids import get_current_ids
from baseball_spider.spider.selenium_manager import create_driver


def get_player_bio(
    player_id: str,
    driver: Optional['selenium.webdriver.chrome.webdriver.WebDriver'] = None,
    ) -> dict:
    '''
    Queries baseballsavant.mlb.com to get biographical information on a player.

    args:
        player_id: mlb.com player ID for given player
        driver: selenium webdriver being used to connect to the website

    returns:
        info_dict: dictionary of player info
    '''
    try:
        info_df = pd.read_csv('data/player_bios.csv')
        info_dict = info_df.loc[info_df.player_id.eq(player_id)].to_dict('records')[0]
        if len(info_dict['player_id']) > 1:
            return info_dict
    except:
        print('player_bios.csv either does not exist or player is not in it.')
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

    return info_dict


def get_all_bios(
    driver: Optional['selenium.webdriver.chrome.webdriver.WebDriver'] = None,
    logger: Optional['logging.Logger'] = None
    ) -> pd.DataFrame:
    '''
    Gets all bios from exisiting bios file or pulls bios from web if file DNE.

    args:
        driver: optional selenium webdriver if bios need to be scraped
        logger: logger to track webscraping

    returns:
        bios_df: Pandas DataFrame of all player bios
    '''
    try:
        bios_df = pd.read_csv('data/player_bios.csv')
        return bios_df
    except:
        print('player_bios.csv either does not exist or player is not in it.')
    ids = get_current_ids(driver if driver else None)
    final_info = {'player_id':[], 'name':[], 'position':[]}
    for player_id in ids.player_id:
        info = get_player_bio(player_id, driver)
        logger.info(f'Bio for {info["name"]} gathered.')
        final_info['player_id'].append(info['player_id'])
        final_info['name'].append(info['name'])
        final_info['position'].append(info['position'])
    bios_df = pd.DataFrame(final_info)
    bios_df.to_csv(f'data/player_bios.csv', index=False)

    return bios_df