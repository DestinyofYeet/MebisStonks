from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
import logging


class Interface:
    def __init__(self, username, password, abgabe_url, debug=False):
        self.url = "https://lernplattform.mebis.bayern.de"
        self.logger = logging.getLogger("Interface")
        self.username = username
        self.password = password
        self.abgabe_url = abgabe_url
        self.debug = debug
        self.driver = None
        self.start_driver()

    def start_driver(self):
        # starts the driver
        logger = self.logger
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
        logger.debug("Adding options successfull")

        # routes the chromedriver output to the corresponding nul output
        if sys.platform.startswith("win"):
            self.driver = webdriver.Chrome("chromedriver.exe", options=options, service_log_path='NUL')
        else:
            self.driver = webdriver.Chrome("chromedriver", options=options, service_log_path='/dev/null')

        logger.debug(f"Python {sys.version} on {sys.platform}")

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

        self.logger.info("Erfolgreich in Mebis eingeloggt!")

    def download_page(self, path=None):
        # checks if a specific path is given, if not, its just downloading the webpage to the main directory
        logger = self.logger
        if path is None:
            with open("page.html", 'w+', encoding='utf-8') as f:
                f.write(self.driver.page_source)
        logger.info("Seite wurde erfolgreich heruntergeladen.")

    def main_program(self):
        # main program

        # goes to the url its supposed to check that you were there
        self.driver.get(self.abgabe_url)

    def close_driver(self):
        # closes the driver
        logger = self.logger
        logger.info("Webbrowser wurde geschlossen.")
        self.driver.close()

