from tools.interface import Interface
from datetime import datetime
import time
import configparser
import tools.Exceptions as Exceptions
import logging
import os
import shutil


def setup_logging():
    # setup logging to console and to file

    if not os.path.exists("logs/"):
        os.mkdir("logs/")
    if os.path.exists("logs/tmp/"):
        shutil.rmtree("logs/tmp/")
    numbers = [0]
    for i in os.listdir("logs/"):
        if i.endswith(".zip"):
            continue
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

    _, _, should_zip = load_config()
    # compresses all logs from the previous day to one zip file
    if not should_zip:
        logging.getLogger('main').info("Das Zippen der logs wird übersprungen.")
    zipped = False
    current_date = datetime.now().strftime("%d.%m.%Y")
    current_day = int(datetime.now().strftime("%d"))
    current_month = int(datetime.now().strftime("%m"))
    current_year = int(datetime.now().strftime("%Y"))
    files_to_compress = []
    for i in os.listdir("logs/"):
        if i.endswith(".zip"):
            continue
        file_day = int(i.split("log.", 1)[-1].split(".", 1)[0])
        file_month = int(i.split("log.", 1)[-1].split(".", 1)[-1].split(".", 1)[0])
        file_year = int(i.split("log.", 1)[-1].split(".", 1)[-1].split(".", 1)[-1].split("-")[0])

        if file_year != current_year:
            files_to_compress.append(i)
        elif file_month != current_month:
            files_to_compress.append(i)
        elif file_day != current_day:
            files_to_compress.append(i)

    while len(files_to_compress) > 0:
        file = files_to_compress[0]
        date = file.split("log.", 1)[-1].rsplit("-")[0]
        similar_files = [i for i in files_to_compress if i.split("log.", 1)[-1].rsplit("-")[0] == date]
        for i in similar_files:
            files_to_compress.pop(files_to_compress.index(i))

        os.mkdir("logs/tmp/")
        for i in similar_files:
            shutil.move("logs/" + i, "logs/tmp/" + i)
        shutil.make_archive("logs/" + date, "zip", "logs/tmp/")
        zipped = True
        shutil.rmtree("logs/tmp/")

    if zipped:
        logging.getLogger('main').info("Logs wurden gezippt")


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
    data = config["URL-Settings"]

    try:
        if not data["AbgabeUrl"].startswith("https://lernplattform.mebis.bayern.de/"):
            raise Exceptions.InvalidSettingError("Die Einstellung 'AbgabeUrl' wurde entweder falsch konfiguriert!")
    except KeyError:
        raise Exceptions.InvalidSettingError("Die Einstellung 'AbgabeUrl' wurde nicht ausgefüllt!")

    try:
        if config["Webbrowser-Settings"]["Sichtbar"].lower() == "nein":
            debug_value = False
        elif config["Webbrowser-Settings"]["Sichtbar"].lower() == "ja":
            debug_value = True
        else:
            raise Exceptions.InvalidSettingError("Die Einstellung 'Sichtbar' wurde entweder falsch konfiguriert oder wurde nicht ausgefüllt!")
    except KeyError:
        raise Exceptions.InvalidSettingError(
            "Die Einstellung 'Sichtbar' wurde nicht ausgefüllt!")

    try:
        if config["Speicher-Settings"]["Komprimieren"].lower() == "ja":
            compress = True
        elif config["Speicher-Settings"]["Komprimieren"].lower() == "nein":
            compress = False
        else:
            raise Exceptions.InvalidSettingError("Die Einstellung 'Komprimieren' wurde entweder falsch konfiguriert!")
    except KeyError:
        Exceptions.InvalidSettingError("Die Einstellung 'Komprimieren' wurde nicht ausgefüllt!")

    logger.debug("Konfigurationsdatei wurde eingelesen")
    return data["AbgabeUrl"], debug_value, compress


def main():
    # main file
    setup_logging()
    logger = logging.getLogger('main')
    username, password = load_userdata()
    abgabe_url, debug_value, _ = load_config()

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
