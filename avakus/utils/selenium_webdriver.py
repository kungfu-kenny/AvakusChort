import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from contextlib import contextmanager


@contextmanager
def Driver(url: str):
    options = Options()
    options.headless = True
    seleniumLogger.setLevel(logging.WARNING)
    driver = webdriver.Firefox(
        options=options,
        executable_path="geckodriver/geckodriver",
        service_log_path=os.devnull,
    )
    driver.set_page_load_timeout(60)
    try:
        driver.get(url)
        yield driver
    finally:
        driver.close()