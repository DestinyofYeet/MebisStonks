from tools.interface import Interface
import json
from datetime import datetime
import time
import os


def load_userdata():
    # loads userdata
    with open("config/userdata.json") as f:
        config = json.load(f)

    return config["username"], config["password"]


def load_config():
    # loads config
    with open("config/config.json") as f:
        config = json.load(f)

    return config["abgabe-url"]


username, password = load_userdata()
abgabe_url = load_config()

# checks if time is between 8:00 and 8:15 o'clock to log you in and to check you off

while True:
    if int(datetime.now().strftime("%H")) == 8 and 0 < int(datetime.now().strftime("%M")) < 15:
        print("My time has come...")
        break
    else:
        print(f"Waiting 5 more mins, current time is {datetime.now().strftime('%H:%M')}")
        time.sleep(300)


# starts the main browser, the debug option just tells the script to show the chrome screen or to not show it
bot = Interface(username, password, abgabe_url, debug=True)


bot.main_program()
bot.download_page()
bot.close_driver()
