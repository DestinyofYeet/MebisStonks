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
        # starts the driver
        options = webdriver.ChromeOptions()
        if not self.debug:
            # either show or not show the chrome-driver
            options.add_argument('headless')
        # just some options to make it more smoothly and to make it output less
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        options.add_argument("start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # routes the chromedriver output to the corresponding nul output
        if sys.platform.startswith("win"):
            self.driver = webdriver.Chrome("chromedriver.exe", options=options, service_log_path='NUL')
        else:
            self.driver = webdriver.Chrome("chromedriver", options=options, service_log_path='/dev/null')

        # goes to self.url
        self.driver.get(self.url)

        # logs in
        self.perform_login()

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

    def download_page(self, path=None):
        # checks if a specific path is given, if not, its just downloading the webpage to the main directory
        if path is None:
            with open("page.html", 'w+', encoding='utf-8') as f:
                f.write(self.driver.page_source)

    def main_program(self):
        # main program

        # goes to the url its supposed to check that you were there
        self.driver.get(self.abgabe_url)

    def close_driver(self):
        # closes the driver
        self.driver.close()
