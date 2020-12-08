from MebisStonks.tools import interface
import json


def load_userdata():
    with open("config/userdata.json") as f:
        config = json.load(f)

    return config["username"], config["password"]


def load_config():
    with open("config/config.json") as f:
        config = json.load(f)

    return config["abgabe-url"]


username, password = load_userdata()
abgabe_url = load_config()
bot = interface.Interface(username, password, abgabe_url, debug=True)

bot.close_driver()
