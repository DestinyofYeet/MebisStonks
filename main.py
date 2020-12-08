from tools.interface import Interface
from datetime import datetime
import time
import configparser
import tools.Exceptions as Exceptions
import logging
import os


def setup_logging():
    # setup logging to console and to file
    numbers = [0]
    for i in os.listdir("logs/"):
        ending = i.rsplit("-")[-1]
        numbers.append(int(ending.rsplit(".txt")[0]))
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s [%(levelname)s]: %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=f'logs/log.{datetime.now().strftime("%d.%m.%Y")}-{max(numbers) + 1}.txt',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    logging.debug("Logging setup done!")


def load_userdata():
    # loads userdata
    logger = logging.getLogger('main')
    config = configparser.ConfigParser()
    config.read("config/Benutzerdaten.ini")
    data = config["UserData"]

    try:
        username = data["Benutzername"]
        password = data["Passwort"]
    except KeyError:
        raise Exceptions.InvalidSettingError("Entweder wurde das Passwort- oder das Benutzernamenfeld ausgelassen!")

    logger.debug("Benutzerdaten wurden eingelesen")
    return username, password


def load_config():
    # loads config and checks for errors
    logger = logging.getLogger('main')
    config = configparser.ConfigParser()
    config.read("config/Einstellung.ini")
    data = config["URL-Section"]

    if data["Sichtbar"].lower() == "nein":
        debug_value = False
    elif data["Sichtbar"].lower() == "ja":
        debug_value = True
    else:
        raise Exceptions.InvalidSettingError("Die Einstellung 'Sichtbar' wurde entweder falsch konfiguriert oder wurde nicht ausgefüllt!")

    if not data["AbgabeUrl"].startswith("https://lernplattform.mebis.bayern.de/"):
        raise Exceptions.InvalidSettingError("Die Einstellung 'AbgabeUrl' wurde entweder falsch konfiguriert oder wurde nicht ausgefüllt!")

    logger.debug("Konfigurationsdatei wurde eingelesen")
    return data["AbgabeUrl"], debug_value


def main():
    # main file
    setup_logging()
    logger = logging.getLogger('main')
    username, password = load_userdata()
    abgabe_url, debug_value = load_config()

    # checks if time is between 8:00 and 8:15 o'clock to log you in and to check you off

    while True:
        if int(datetime.now().strftime("%H")) == 8 and 0 < int(datetime.now().strftime("%M")) < 15:
            logger.info("Zeit erreicht...")
            break
        else:
            logger.info(
                f"Warte 5 weitere minuten bis die Zeit zwischen 8:00 Uhr und 8:15 Uhr ist... Aktuelle Zeit: {datetime.now().strftime('%H:%M')}")
            time.sleep(300)

    # starts the main browser, the debug option just tells the script to show the chrome screen or to not show it
    bot = Interface(username, password, abgabe_url, debug=debug_value)
    bot.main_program()
    bot.download_page()
    bot.close_driver()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error("Error in main thread:", exc_info=True)
