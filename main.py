from tools.interface import Interface
from datetime import datetime
import time
import configparser
import tools.Exceptions as Exceptions


def load_userdata():
    # loads userdata
    config = configparser.ConfigParser()
    config.read("config/Benutzerdaten.ini")
    data = config["UserData"]

    try:
        username_input = data["Benutzername"]
        password_input = data["Passwort"]
    except KeyError:
        raise Exceptions.InvalidSettingError("Entweder wurde das Passwort- oder das Benutzernamenfeld ausgelassen!")

    return username_input, password_input


def load_config():
    # loads config and checks for errors
    config = configparser.ConfigParser()
    config.read("config/Einstellung.ini")
    data = config["URL-Section"]

    if data["Sichtbar"].lower() == "nein":
        debug_value1 = False
    elif data["Sichtbar"].lower() == "ja":
        debug_value1 = True
    else:
        raise Exceptions.InvalidSettingError("Die Einstellung 'Sichtbar' wurde entweder falsch konfiguriert oder wurde nicht ausgefüllt!")

    if not data["AbgabeUrl"].startswith("https://lernplattform.mebis.bayern.de/"):
        raise Exceptions.InvalidSettingError("Die Einstellung 'AbgabeUrl' wurde entweder falsch konfiguriert oder wurde nicht ausgefüllt!")

    return data["AbgabeUrl"], debug_value1


username, password = load_userdata()
abgabe_url, debug_value = load_config()

# checks if time is between 8:00 and 8:15 o'clock to log you in and to check you off

while True:
    if int(datetime.now().strftime("%H")) == 8 and 0 < int(datetime.now().strftime("%M")) < 15:
        print("Zeit erreicht...")
        break
    else:
        print(f"Warte 5 weitere minuten bis die Zeit zwischen 8:00 Uhr und 8:15 Uhr ist... Aktuelle Zeit: {datetime.now().strftime('%H:%M')}")
        time.sleep(300)


# starts the main browser, the debug option just tells the script to show the chrome screen or to not show it
bot = Interface(username, password, abgabe_url, debug=debug_value)


bot.main_program()
bot.download_page()
bot.close_driver()
