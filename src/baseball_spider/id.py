from datetime import datetime as dt
from glob import glob
import pandas as pd
from typing import Optional, Dict, Any, TYPE_CHECKING
from selenium_manager import create_driver
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from selenium import webdriver


def get_mlb_ids(
        return_data: bool = True,
        save_path: str = None,
        driver: 'webdriver' = None,
        ) -> Dict[str, Any]:
    '''
    Collects all player IDs availble on MLB.com. Details on which IDs are
    available aren't available, but it seems to be all active players.

    args:
        return_data: bool to determine if anything will be returned
        save_path: path to save IDs to, if none, IDs will not be saved
        driver: selenium webdriver used to connect to the website

    returns:
        id_dict: dictionary of player IDs
    '''
    if not driver:
        driver = create_driver()

    id_dict = {'player_id': [str]}
    player_list_url = 'https://www.mlb.com/players'
    driver.get(player_list_url)
    player_links = driver.find_elements(By.CLASS_NAME, 'p-related-links__link')

    for player in player_links:
        player_id = player.get_attribute('href').split('/')[-1]
        if len(player_id.split('-')) != 3:
            continue
        id_dict['player_id'].append(player_id)

    driver.close()
    if save_path:
        new_players_df = pd.DataFrame(id_dict)
        new_players_df.to_csv(save_path, index=False)
    if return_data:
        return id_dict
