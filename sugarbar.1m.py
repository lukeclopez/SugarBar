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
DIRECTIONS = {
    "Flat": "steady",
    "FortyFiveUp": "rising",
    "FortyFiveDown": "falling",
    "SingleUp": "single up",
    "DoubleUp": "double up",
    "SingleDown": "single down",
    "DoubleDown": "double down",
    "NONE": "no slope",
    "NOT_COMPUTABLE": "the slope is not computable",
    "RATE_OUT_OF_RANGE": "the rate is out of range"
}

def refresh():
    sugar_mgdl, direction = get_reading()
    display(sugar_mgdl, direction)



def get_reading():
    res = requests.get(BASE_URL + ENDPOINT + TOKEN)

    if res.status_code != 200:
        return (res.status_code, res.reason)

    data = json.loads(res.content)[0]
    sugar_mgdl = get_sugar_level(data)
    direction = get_direction(data)
    return (sugar_mgdl, direction)
    

def display(sugar_mgdl, direction):
    display_string = f":drop_of_blood: {sugar_mgdl} {direction} | href={BASE_URL} | color={get_color(sugar_mgdl)}"
    print(display_string)

def get_sugar_level(data):
    str(data["sgv"])

def get_direction(data):
    return DIRECTIONS.get(data["direction"], "no direction found")

def get_color(sugar_mgdl):
    return "blue"

if __name__ == "__main__":
    refresh()