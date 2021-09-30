from datetime import datetime as dt
from glob import glob
import pandas as pd
from typing import Optional

def get_current_ids(
    driver: Optional['selenium.webdriver.chrome.webdriver.WebDriver'] = None
    ) -> pd.DataFrame:
    '''
    Gets latest CSV of player/player_ids and checks to see if it needs to be
    updated via mlb.com.

    args:
        driver: optional selenium webdriver to connect to the website

    returns:
        players_df: Pandas DataFrame of player names and IDs
    '''
    id_files = glob('data/mlb_player_ids_*.csv')
    if (
        len(id_files) == 0 
        or int(id_files[-1].split('_')[-1].split('-')[0]) < dt.now().year
        and driver
        ):
        update_players(driver)
        id_files = glob('data/mlb_player_ids_*.csv')

    try:
        players_df = pd.read_csv(id_files[-1])
    except Exception as e:
        raise Exception('No player IDs available to read. Check file location \
            or include a driver to scrape new player IDs.')

    return players_df


def update_players(
    driver: 'selenium.webdriver.chrome.webdriver.WebDriver'
    ):
    '''
    Updates the player ID CSV by pulling a list of all players on mlb.com, 
    retrieving their player IDs and visiting their page to get their information.
    
    args:
        driver: selenium webdriver used to connect to the website
    '''
    player_dict = {'name':[str], 'player_id':[str]}
    player_list_url = 'https://www.mlb.com/players'
    driver.get(player_list_url)
    player_links = driver.find_elements_by_class_name('p-related-links__link')
    
    for player in player_links:
        name = player.text
        player_id = player.get_attribute('href').split('/')[-1]
        player_dict['name'].append(name)
        player_dict['player_id'].append(player_id)

    new_players_df = pd.DataFrame(player_dict)
    new_players_df.to_csv(
        f'data/mlb_player_ids_{dt.now().year}-{dt.now().month}.csv',
        index=False
        )