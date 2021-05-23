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

BASE_URL = "http://luke-lopez-cgm.herokuapp.com"
ENDPOINT = "/api/v1/entries/sgv.json"
TOKEN = "?token=" + API_KEY
EMOJI_DROP_OF_BLOOD = "\U0001FA78"
BG_TARGET_BOTTOM = 80
BG_TARGET_TOP = 180

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

COLORS = {
    "okay": "white",
    "high": "yellow",
    "low": "red"
}

def refresh():
    sugar_mgdl, direction = get_reading_data()
    display(sugar_mgdl, direction)

# Helpers

def get_reading_data():
    res = requests.get(BASE_URL + ENDPOINT + TOKEN)

    if res.status_code != 200:
        return (res.status_code, res.reason)

    data = json.loads(res.content)[0]
    sugar_mgdl = get_sugar_level(data)
    direction = get_direction(data)
    return (sugar_mgdl, direction)

def get_sugar_level(data):
    return str(data["sgv"])

def get_direction(data):
    return data.get("direction")

def display(sugar_mgdl, direction):
    display = f"{EMOJI_DROP_OF_BLOOD} {sugar_mgdl} {get_direction_indicator(direction)}"
    display_string = f"{display} | href={BASE_URL} | color={get_color(sugar_mgdl)}"
    print(display_string)

def get_direction_indicator(direction):
    return DIRECTIONS.get(direction, "E")

def get_color(sugar_mgdl):
    sugar_mgdl = int(sugar_mgdl)
    status = "okay" if sugar_mgdl > BG_TARGET_BOTTOM else "low"
    status = "high" if sugar_mgdl >= BG_TARGET_TOP else status
    return COLORS[status]

if __name__ == "__main__":
    refresh()