import pandas as pd
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from typing import Optional, Dict, Any, Sequence, Type, TYPE_CHECKING
from selenium_manager import create_driver

if TYPE_CHECKING:
    import logging
    from selenium import webdriver


def get_bios(
        player_id: str,
        return_data: bool = True,
        save_path: str = None,
        driver: Optional['webdriver'] = None,
        ) -> Dict[str, str]:
    '''
    Queries baseballsavant.mlb.com to get biographical information on a player.

    args:
        player_id: mlb.com player ID for given player
        filepath: filepath for all locally stored data
        webscrape: if webscrape, then create a driver if one is not provided
                   for scraping
        driver: selenium webdriver being used to connect to the website

    returns:
        info_dict: dictionary of player info
    '''
    if not driver:
        driver = create_driver()

    if type(player_id) is str:
        player_id = [player_id, ]

    bio_dict = {
        'player_id': [],
        'name': [],
        'position': [],
        'b/t': [],
        'age': [],
    }
    for player in player_id:
        url = f'https://baseballsavant.mlb.com/savant-player/{player}'
        try:
            driver.get(url)
        except InvalidSessionIdException:
            driver = create_driver()
            driver.get(url)
        info_div = driver.find_element(By.CLASS_NAME, 'bio-player-name')
        details_row = info_div.find_element(By.XPATH, 'div[2]').text
        details = details_row.split('|')
        bio_dict['player_id'].append(player)
        bio_dict['name'].append(info_div.find_element(By.XPATH, 'div[1]').text)
        bio_dict['position'].append(details[0].strip().split()[0])
        bio_dict['b/t'].append(details[1].strip().split()[-1])
        bio_dict['age'].append(details[-1].strip().split()[-1])
        if bio_dict['position'] in ('LF', 'RF', 'CF'):
            bio_dict['position'] = 'OF'
    
    driver.close()
    if save_path:
        bio_df = pd.DataFrame(bio_dict)
        bio_df.to_csv(save_path, index=False)
    if return_data:
        return bio_dict
