from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time


class Interface:
    def __init__(self, username, password, abgabe_url, debug=False):
        self.url = "https://lernplattform.mebis.bayern.de"
        self.username = username
        self.password = password
        self.abgabe_url = abgabe_url
        self.debug = debug
        self.driver = None
        self.start_driver()

    def start_driver(self):
        options = webdriver.ChromeOptions()
        if not self.debug:
            options.add_argument('headless')
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if sys.platform.startswith("win"):
            self.driver = webdriver.Chrome(options=options, service_log_path='NUL')
        else:
            self.driver = webdriver.Chrome(options=options, service_log_path='/dev/null')

        self.driver.get(self.url)
        self.perform_login()
        self.main_program()

    def perform_login(self):
        # tabs to the 'insert username field'
        action = ActionChains(self.driver)
        action.send_keys(Keys.TAB)
        action.send_keys(self.username)
        action.perform()

        # tabs to the 'insert password field' and input stuff
        action = ActionChains(self.driver)
        action.send_keys(Keys.TAB)
        action.send_keys(self.password)
        action.perform()
        time.sleep(0.5)

        # hits enter to login
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER)
        action.perform()
        time.sleep(0.5)

    def main_program(self):
        self.driver.get(self.abgabe_url)

    def close_driver(self):
        self.driver.close()
