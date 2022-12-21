#!/opt/homebrew/bin/python3
# coding=utf-8
#
# <xbar.title>Dexcom Blood Sugar</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>lukeclopez</xbar.author>
# <xbar.author.github>lukeclopez</xbar.author.github>
# <xbar.desc>Displays my blood sugar from Dexcom</xbar.desc>
# <xbar.image>https://i.imgur.com/I3MdNmU.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.dependencies>pydexcom python package</xbar.dependencies>
#
# by lukeclopez

from pydexcom import Dexcom
from secret_info import USERNAME, PASSWORD

dexcom = Dexcom(USERNAME, PASSWORD)

EMOJI_DROP_OF_BLOOD = "\U0001FA78"
BG_TARGET_BOTTOM = 80
BG_TARGET_TOP = 180

# Calculated value -> the color the number and arrow will be
COLORS = {
    "okay": "white",
    "high": "yellow",
    "low": "red"
}


def refresh():
    sugar_mgdl, direction, delta, latest_reading_time = get_reading_data()
    display(sugar_mgdl, direction, delta, latest_reading_time)


# Helpers


def get_reading_data():
    minutes = 30
    max_count = 2
    bg_readings = dexcom.get_glucose_readings(minutes, max_count)

    latest = bg_readings[0]
    previous = bg_readings[-1]

    sugar_mgdl = latest.mg_dl
    direction = latest.trend_arrow
    delta = latest.mg_dl - previous.mg_dl if len(bg_readings) == 2 else 999
    latest_reading_time = latest.times

    return (sugar_mgdl, direction, delta, latest_reading_time)


def display(sugar_mgdl, direction, delta, latest_reading_time):
    display = f"{EMOJI_DROP_OF_BLOOD} {sugar_mgdl} {direction}"
    options = f"| color={get_color(sugar_mgdl)}"
    display_string = f"{display} {options}"
    print(display_string)
    print("---")
    print(f"{display_delta(delta)} from previous")
    print(f"Latest reading time: {latest_reading_time}")


def display_delta(delta):
    return f"+{delta}" if delta > 0 else delta


def get_color(sugar_mgdl):
    sugar_mgdl = int(sugar_mgdl)
    status = "okay" if sugar_mgdl > BG_TARGET_BOTTOM else "low"
    status = "high" if sugar_mgdl >= BG_TARGET_TOP else status
    return COLORS[status]


if __name__ == "__main__":
    refresh()