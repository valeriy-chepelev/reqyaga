from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def _wait_page(drv):
    WebDriverWait(driver=drv, timeout=20).until(
        lambda x: x.execute_script("return document.readyState === 'complete'"))


def _wait_data(drv):
    element_present = EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.TransformedHtml.PageDoc-Content.PageDoc-Content_type_wysiwyg'))  # tuple required
    WebDriverWait(drv, 10).until(element_present)


def login(config):
    """
    Logins to Yandex Wiki using credentials from config
    :param config: dictionary with credentials 'login', 'password', 'checkin'
    :return: webdriver with logged-in Wiki root page
    """

    # Create Chrome Options and Service
    service = Service(executable_path='chromedriver.exe')
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple"
                         "WebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--password-store=basic")
    options.add_argument("--no-sandbox")

    # Start Chrome Driver
    drv = webdriver.Chrome(service=service, options=options)

    # enter login page
    drv.get("https://wiki.yandex.ru/?skipPromo=1")
    _wait_page(drv)

    # select login using Yandex ID
    drv.find_element(By.CSS_SELECTOR,
                     "button.g-button.g-button_view_action.g-button_size_l."
                     "g-button_pin_round-round.auth-button.login-form__button").click()
    _wait_page(drv)

    # enter credentials
    entry = drv.find_element(By.CSS_SELECTOR, "#passp-field-login")
    entry.send_keys(config['login'])
    entry.submit()
    _wait_page(drv)
    sleep(1)
    entry = drv.find_element(By.CSS_SELECTOR, "#passp-field-passwd")
    entry.send_keys(config['password'])
    entry.submit()
    _wait_data(drv)

    # check wiki root page loaded
    assert config['checkin'] in drv.page_source

    return drv


def tables(drv):
    t = drv.find_elements(By.XPATH, '//table')
    print(f"{len(t)} tables found.")


cfg = read_config('reqyaga.ini')
driver = login(cfg)
# open data page
driver.get("https://wiki.yandex.ru/mt/mt-rd/ff-e710f1/prorabotka-konstruktiva/"
           "1.4.-moduli-binarnyx-signalov-mbs-ili-vxodovvyxodo/2.4.1.-trebovanija-k-mvv/")
_wait_data(driver)
tables(driver)
input('Press enter')
