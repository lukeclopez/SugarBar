#!/usr/bin/env python
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



print("Hey you")