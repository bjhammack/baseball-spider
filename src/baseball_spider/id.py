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
        ):
    '''
    Updates the player ID CSV by pulling a list of all players on mlb.com,
    retrieving their player IDs and visiting their page to get their information.

    args:
        parent_data_dir: parent folder for all locally stored data
        driver: selenium webdriver used to connect to the website
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
