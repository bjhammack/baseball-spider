from typing import Optional
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


def create_driver(
    driver_path: Optional[str] = None,
    driver_options: Optional['selenium.webdriver.options'] = None # type: ignore
    ) -> webdriver:
    '''
    Prepare Selenium webdriver for scraping and setting chromedriver arguments
    
    Args:
        driver_path: path to user defined webdriver. If none, driver is created
        driver_options: options for driver, otherwise uses defaults
        
    Returns:
        selenium driver for webscraping
        logger for logging results
    '''
    if driver_options:
        options = driver_options
    else:
        options = webdriver.chrome.options.Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--log-level=0')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')

    if driver_path:
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
    else:
        driver = webdriver.Chrome(
            ChromeDriverManager(
                '93.0.4577.63',
                log_level=0,
                print_first_line=False,
                ).install(),
            options=options)

    return driver