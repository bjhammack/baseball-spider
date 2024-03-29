from numpy.testing import assert_equal  # used when nans may be present in result
from pandas import read_csv
import pytest
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from baseball_spider.spider.statcast import at_bats


def test_existing_at_bats(trea_2021):
    test_at_bats = at_bats.get_player_abs(
        player_id_season = ('trea-turner-607208', 2021),
        existing_data_folder_path = 'tests/test_data/at_bats/',
        player_bios_path = 'tests/test_data/player_bios.csv',
        webscrape = False,
        )[0]
    assert_equal(test_at_bats, trea_2021)


def test_save_at_bats(tmpdir, trea_2021):
    save_location_folder = tmpdir.mkdir('player')
    at_bats.get_player_abs(
        player_id_season = ('trea-turner-607208', 2021),
        existing_data_folder_path = 'tests/test_data/at_bats/',
        player_bios_path = 'tests/test_data/player_bios.csv',
        webscrape = False,
        save_folder_path = save_location_folder,
        return_data = False,
        )
    save_location = save_location_folder.join('trea-turner-607208_2021.csv')
    saved_data = read_csv(save_location).to_dict('list')
    assert len(save_location_folder.listdir()) == 1
    assert_equal(saved_data, trea_2021)


def test_save_at_bats_no_data(tmpdir):
    expected_keys = ('player_id', 'date', 'opponent', 'result', 'ev', 'la',
        'distance', 'direction', 'pitch_velo', 'pitch_type')
    save_location = tmpdir.mkdir('player').join('player-000000_2021.csv')
    with pytest.raises(ValueError) as e:
        at_bats.save_at_bats({k:[] for k in expected_keys}, save_location)
    print(e.value)
    assert 'The at bat dictionary is empty' in str(e.value)


def test_save_at_bats_empty(tmpdir):
    save_location = tmpdir.mkdir('player').join('player-000000_2021.csv')
    with pytest.raises(ValueError) as e:
        at_bats.save_at_bats({}, save_location)
    print(e.value)
    assert 'Expected dictionary with keys' in str(e.value)


def test_bad_player_id_no_scraping():
    with pytest.raises(IndexError):
        at_bats.get_player_abs(
            player_id_season = ('Player does not exist.', 2020),
            existing_data_folder_path = 'tests/test_data/at_bats/',
            player_bios_path = 'tests/test_data/player_bios.csv',
            webscrape = False,
            )


def test_bad_season_no_scraping():
    with pytest.raises(FileNotFoundError):
        at_bats.get_player_abs(
            player_id_season = ('trea-turner-607208', 1999),
            existing_data_folder_path = 'tests/test_data/at_bats/',
            player_bios_path = 'tests/test_data/player_bios.csv',
            webscrape = False,
            )


def test_bad_parent_data_dir_no_scraping():
    with pytest.raises(FileNotFoundError):
        at_bats.get_player_abs(
            player_id_season = ('trea-turner-607208', 2020),
            existing_data_folder_path = 'tests/test_data_fake/at_bats',
            player_bios_path = 'tests/test_data/player_bios.csv',
            webscrape = False,
            )


def test_scraping_timeout():
    with pytest.raises(TimeoutException):
        at_bats.get_player_abs(
            player_id_season = ('dummy-player-000000/badsite.org ', 2021),
            player_bios_path = 'tests/test_data/player_bios.csv',
            )


# def test_scraping_at_bats_no_driver(bummer_2020):
#     test_at_bats = at_bats.get_player_abs(
#         player_id_season = ('aaron-bummer-607481', 2020),
#         existing_data_folder_path = 'tests/test_data/at_bats/',
#         webscrape = True,
#         ignore_files = True,
#         driver = None,
#         )[0]
#     assert_equal(test_at_bats, bummer_2020)


# def test_scraping_at_bats_with_driver(bummer_2020, driver):
#     test_at_bats = at_bats.get_player_abs(
#         player_id_season = ('aaron-bummer-607481', 2020),
#         existing_data_folder_path = 'tests/test_data/at_bats/',
#         webscrape = True,
#         ignore_files = True,
#         driver = driver,
#         )[0]
#     assert_equal(test_at_bats, bummer_2020)


# def test_scraping_at_bats_missing_file_with_driver(bummer_2020, driver):
#     test_at_bats = at_bats.get_player_abs(
#         player_id_season = ('aaron-bummer-607481', 2020),
#         existing_data_folder_path = 'tests/test_data/fake_at_bats/',
#         webscrape = True,
#         ignore_files = True,
#         driver = driver,
#         )[0]
#     assert_equal(test_at_bats, bummer_2020)


# def test_scraping_at_bats_bad_id(driver):
#     with pytest.raises(NoSuchElementException):
#         test_at_bats = at_bats.get_player_abs(
#             player_id_season = ('aaron-bummer-000000', 2020),
#             existing_data_folder_path = 'tests/test_data/at_bats/',
#             webscrape = True,
#             ignore_files = False,
#             player_bios_path = 'tests/test_data/player_bios.csv',
#             driver = driver,
#             )
