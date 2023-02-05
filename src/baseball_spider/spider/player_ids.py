from datetime import datetime as dt
from glob import glob
import pandas as pd
from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from selenium import webdriver


def _get_current_ids(
        parent_data_dir: Optional[str] = None,
        driver: Optional['webdriver'] = None
        ) -> Dict[Any, Any]:
    '''
    Gets latest CSV of player/player_ids and checks to see if it needs to be
    updated via mlb.com.

    args:
        parent_data_dir: parent folder for all locally stored data
        driver: optional selenium webdriver to connect to the website

    returns:
        players: Dictionary of player IDs
    '''
    id_files = glob(f'{parent_data_dir}/mlb_player_ids_*.csv')
    if (
        driver
        and parent_data_dir
        and (
            len(id_files) == 0
            or int(id_files[-1].split('_')[-1].split('-')[0]) < dt.now().year
            )
            ):
        _update_players(parent_data_dir, driver)
        id_files = glob(f'{parent_data_dir}/mlb_player_ids_*.csv')

    try:
        players = pd.read_csv(id_files[-1]).to_dict('list')
    except Exception:
        raise Exception('No player IDs available to read. Check file location \
            or include a driver to scrape new player IDs.')

    return players


def _update_players(
        parent_data_dir: Optional[str],
        driver: 'webdriver'
        ):
    '''
    Updates the player ID CSV by pulling a list of all players on mlb.com,
    retrieving their player IDs and visiting their page to get their information.

    args:
        parent_data_dir: parent folder for all locally stored data
        driver: selenium webdriver used to connect to the website
    '''
    player_dict = {'player_id': [str]}
    player_list_url = 'https://www.mlb.com/players'
    driver.get(player_list_url)
    player_links = driver.find_elements_by_class_name('p-related-links__link')

    for player in player_links:
        player_id = player.get_attribute('href').split('/')[-1]
        player_dict['player_id'].append(player_id)

    new_players_df = pd.DataFrame(player_dict)
    new_players_df.to_csv(
        f'{parent_data_dir}/mlb_player_ids_{dt.now().year}-{dt.now().month}.csv',
        index=False
        )
