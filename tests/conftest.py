from numpy import nan
from pandas import read_csv
import pytest

from baseball_spider.spider.selenium_manager import create_driver


@pytest.fixture
def trea_2021():
    at_bats = {
        'player_id':['trea-turner-607208', 'trea-turner-607208', 'trea-turner-607208',
            'trea-turner-607208', 'trea-turner-607208'],
        'date':['4/7/2021', '4/6/2021', '4/6/2021', '4/6/2021', '4/6/2021'],
        'opponent':['Fried, Max', 'Smith, Will', 'Smyly, Drew', 'Smyly, Drew',
            'Smyly, Drew'],
        'result':['double', 'hit_by_pitch', 'field_out', 'home_run', 'strikeout'],
        'ev':[104.2, nan, 100.3, 101.6, nan],
        'la':[11.0, nan, -17.0, 26.0, nan],
        'distance':[256.0, nan, 8.0, 402.0, nan],
        'direction':['Straightaway', nan, 'Pull', 'Pull', nan],
        'pitch_velo':[76.2, 82.1, 93.4, 91.7, 94.3],
        'pitch_type':['Curveball', 'Slider', '4-Seam Fastball', '4-Seam Fastball',
            '4-Seam Fastball'],
    }
    return at_bats


@pytest.fixture
def bummer_2020():
    '''
    Minor changes need to be made to the file data, as it is scraped as all strings.
    '''
    at_bats = read_csv('tests/test_data/at_bats/P/aaron-bummer-607481_2020.csv')
    at_bats = at_bats.fillna('').astype(str)
    at_bats['la'] = at_bats['la'].str.split('.', expand=True)[0]
    at_bats['distance'] = at_bats['distance'].str.split('.', expand=True)[0]
    return at_bats.to_dict('list')
