from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import configparser
from time import sleep


def read_config(filename):
    """
    Read 'DEFAULT' from configuration file, asserts 'login' present
    :param filename: Ini-file filename
    :return: DEFAULT config section
    """
    config = configparser.ConfigParser()
    config.read(filename)
    assert 'login' in config['DEFAULT']
    return config['DEFAULT']


def _wait(w_driver):
    WebDriverWait(driver=w_driver, timeout=20).until(
        lambda x: x.execute_script("return document.readyState === 'complete'"))


def login(config):
    """
    Logins to Yandex Wiki using credentials from config
    :param config: dictionary with credentials 'login', 'password', 'checkin'
    :return: webdriver with logged-in Wiki root page
    """
    service = Service(executable_path='chromedriver.exe')
    drv = webdriver.Chrome(service=service)

    # enter login page
    drv.get("https://wiki.yandex.ru/?skipPromo=1")
    _wait(drv)
    # select login using Yandex ID
    drv.find_element(By.CSS_SELECTOR,
                     "button.g-button.g-button_view_action.g-button_size_l."
                     "g-button_pin_round-round.auth-button.login-form__button").click()
    _wait(drv)
    # enter credentials
    entry = drv.find_element(By.CSS_SELECTOR, "#passp-field-login")
    entry.send_keys(config['login'])
    entry.submit()
    _wait(drv)
    sleep(1)
    entry = drv.find_element(By.CSS_SELECTOR, "#passp-field-passwd")
    entry.send_keys(config['password'])
    entry.submit()
    _wait(drv)
    sleep(
        5)  # TODO: wait for page loaded, see https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    assert config['checkin'] in drv.page_source
    return drv


cfg = read_config('reqyaga.ini')
driver = login(cfg)
# open data page
driver.get("https://wiki.yandex.ru/mt/mt-rd/ff-e710f1/prorabotka-konstruktiva/"
           "1.4.-moduli-binarnyx-signalov-mbs-ili-vxodovvyxodo/2.4.1.-trebovanija-k-mvv/")
_wait(driver)
input('Press enter')
