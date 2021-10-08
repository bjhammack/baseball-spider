from numpy.testing import assert_equal  # used when nans may be present in result
import pytest
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException

from baseball_spider.spider import at_bats


def test_existing_at_bats(trea_2021):
    test_at_bats = at_bats.get_player_abs(
        player_id_season = ('trea-turner-607208', 2021),
        existing_data_folder_path = 'tests/test_data/at_bats/',
        player_bios_path = 'tests/test_data/player_bios.csv',
        webscrape = False,
        )[0]
    assert_equal(test_at_bats, trea_2021)


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


def test_scraping_at_bats_no_driver(bummer_2020):
    test_at_bats = at_bats.get_player_abs(
        player_id_season = ('aaron-bummer-607481', 2020),
        existing_data_folder_path = 'tests/test_data/at_bats/',
        webscrape = True,
        ignore_files = True,
        driver = None,
        )[0]
    assert_equal(test_at_bats, bummer_2020)


def test_scraping_at_bats_with_driver(bummer_2020, driver):
    test_at_bats = at_bats.get_player_abs(
        player_id_season = ('aaron-bummer-607481', 2020),
        existing_data_folder_path = 'tests/test_data/at_bats/',
        webscrape = True,
        ignore_files = True,
        driver = driver,
        )[0]
    assert_equal(test_at_bats, bummer_2020)


def test_scraping_at_bats_missing_file_with_driver(bummer_2020, driver):
    test_at_bats = at_bats.get_player_abs(
        player_id_season = ('aaron-bummer-607481', 2020),
        existing_data_folder_path = 'tests/test_data/fake_at_bats/',
        webscrape = True,
        ignore_files = True,
        driver = driver,
        )[0]
    assert_equal(test_at_bats, bummer_2020)


def test_scraping_at_bats_bad_id(driver):
    with pytest.raises(NoSuchElementException):
        test_at_bats = at_bats.get_player_abs(
            player_id_season = ('aaron-bummer-000000', 2020),
            existing_data_folder_path = 'tests/test_data/at_bats/',
            webscrape = True,
            ignore_files = False,
            player_bios_path = 'tests/test_data/player_bios.csv',
            driver = driver,
            )
