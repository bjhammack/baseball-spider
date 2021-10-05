from numpy.testing import assert_equal  # used when nans may be present in result
import pytest

from baseball_spider.spider import at_bats


def test_existing_at_bats(trea_2021):
    test_at_bats = at_bats.get_at_bats(
        player_id = 'trea-turner-607208',
        season = 2021,
        parent_data_dir = 'tests/test_data/',
        webscrape = False,
        )
    assert_equal(test_at_bats, trea_2021)


def test_bad_player_id_no_scraping():
    with pytest.raises(IndexError):
        at_bats.get_at_bats(
            player_id = 'Player does not exist.',
            season = 2020,
            parent_data_dir = 'tests/test_data/',
            webscrape = False,
            )


def test_bad_season_no_scraping():
    with pytest.raises(FileNotFoundError):
        at_bats.get_at_bats(
            player_id = 'trea-turner-607208',
            season = 1999,
            parent_data_dir = 'tests/test_data/',
            webscrape = False,
            )


def test_bad_parent_data_dir_no_scraping():
    with pytest.raises(FileNotFoundError):
        at_bats.get_at_bats(
            player_id = 'trea-turner-607208',
            season = 2020,
            parent_data_dir = 'tests/test_data_fake/',
            webscrape = False,
            )


def test_scraping_at_bats_no_driver(bummer_2020):
    test_at_bats = at_bats.get_at_bats(
        player_id = 'aaron-bummer-607481',
        season = 2020,
        parent_data_dir = 'tests/test_data/',
        webscrape = True,
        ignore_files = True,
        driver = None,
        )
    assert_equal(test_at_bats, bummer_2020)
