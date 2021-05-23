#!/opt/homebrew/bin/python3
# coding=utf-8
#
# <xbar.title>Dexcom Blood Sugar</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>lukeclopez</xbar.author>
# <xbar.author.github>lukeclopez</xbar.author.github>
# <xbar.desc>Displays my blood sugar from night scout</xbar.desc>
# <xbar.image>https://i.imgur.com/I3MdNmU.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
#
# by lukeclopez

import requests
import json

from secret_info import API_KEY

BASE_URL = "https://luke-lopez-cgm.herokuapp.com"
ENDPOINT = "/api/v1/entries/sgv.json"
TOKEN = "?token=" + API_KEY
EMOJI_DROP_OF_BLOOD = "\U0001FA78"
BG_TARGET_BOTTOM = 80
BG_TARGET_TOP = 180

# Response value from Nightscout -> What will be shown on my menu bar
DIRECTIONS = {
    "Flat": "→",
    "FortyFiveUp": "↗",
    "FortyFiveDown": "↘",
    "SingleUp": "↑",
    "DoubleUp": "⇈",
    "SingleDown": "↓",
    "DoubleDown": "⇊",
    "NONE": "?",
    "NOT_COMPUTABLE": "N/A",
    "RATE_OUT_OF_RANGE": "N/A"
}

# Calculated value -> the color the number and arrow will be
COLORS = {
    "okay": "white",
    "high": "yellow",
    "low": "red"
}

def refresh():
    sugar_mgdl, direction, delta = get_reading_data()
    display(sugar_mgdl, direction, delta)

# Helpers

def get_reading_data():
    res = requests.get(BASE_URL + ENDPOINT + TOKEN)

    if res.status_code != 200:
        return (res.status_code, res.reason)

    data = get_last_data(res.content)
    sugar_mgdl = get_sugar_level(data)
    direction = get_direction(data)
    delta = get_delta(res.content)
    return (sugar_mgdl, direction, delta)

def get_last_data(content):
    return json.loads(content)[0]

def get_sugar_level(data):
    return str(data["sgv"])

def get_direction(data):
    return data.get("direction")

def get_delta(content):
    latest = get_last_data(content)
    second_latest = json.loads(content)[1]
    latest_sugar_level = int(get_sugar_level(latest))
    second_latest_sugar_level = int(get_sugar_level(second_latest))
    return latest_sugar_level - second_latest_sugar_level

def display(sugar_mgdl, direction, delta):
    display = f"{EMOJI_DROP_OF_BLOOD} {sugar_mgdl} {get_direction_indicator(direction)}"
    options = f"| color={get_color(sugar_mgdl)}"
    display_string = f"{display} {options}"
    print(display_string)
    print("---")
    print(f"{display_delta(delta)} from previous")
    print(f"View Nightscout | | href={BASE_URL}")


def get_direction_indicator(direction):
    return DIRECTIONS.get(direction, "E")

def display_delta(delta):
    return f"+{delta}" if delta > 0 else delta

def get_color(sugar_mgdl):
    sugar_mgdl = int(sugar_mgdl)
    status = "okay" if sugar_mgdl > BG_TARGET_BOTTOM else "low"
    status = "high" if sugar_mgdl >= BG_TARGET_TOP else status
    return COLORS[status]

if __name__ == "__main__":
    refresh()