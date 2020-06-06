import datetime

from astropy import units
from astropy.coordinates import get_body, get_sun
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.time import Time
from flask import Flask

Gjovik = EarthLocation.from_geodetic(60.79574, 10.69155)
today = Time.now()
NOW = Time.now().to_datetime()
LIGHT_MINUTE = (1 * units.year).to(units.minute).value

# app = Flask(__name__)


# @app.route("/rand")
# def hei():
#     return str("Hei!")

# if __name__ == "__main__":
# 	app.run(debug=True)


# Name is used to query astropy
# Year is each planet's number of earth years to orbit the sun
planets = [
    {"name": "Mercury", "navn": "Merkur"},
    {"name": "Venus", "navn": "Venus"},
    {"name": "Mars", "navn": "Mars", "year": 365.25 / 687},
    {"name": "Jupiter", "navn": "Jupiter", "year": 12},
    {"name": "Saturn", "navn": "Saturn", "year": 29},
    {"name": "Uranus", "navn": "Uranus", "year": 84},
    {"name": "Neptune", "navn": "Neptun", "year": 165},
    {"name": "Pluto", "navn": "Pluto", "year": 248}
]


def get_light_minutes(body):
    return (body.distance).to(units.lightyear).value * LIGHT_MINUTE


# The planets should have accurate distances, given how much they change in relation to Earth
def get_planet_time(planet):
    body = get_body(planet["name"], today, Gjovik)

    # Get current time minus planet's distance in light minutes
    lm_to_day = get_light_minutes(body) / 1440
    neg_delta = datetime.timedelta(lm_to_day)
    neg_delta_hour = int(str(neg_delta).split(':')[0])
    neg_delta_minute = int(str(neg_delta).split(':')[1])

    # Format hour difference
    if neg_delta_hour == 0:
        neg_delta_hour_text = ""
    elif neg_delta_hour == 1:
        neg_delta_hour_text = "1 time og "
    else:
        neg_delta_hour_text = f"{neg_delta_hour} timer og "

    # Format minute difference
    if neg_delta_minute == 0:
        neg_delta_minute_text = ""
    elif neg_delta_minute == 1:
        neg_delta_minute_text = "1 minutt"
    else:
        neg_delta_minute_text = f"{neg_delta_minute} minutter"

    neg_delta_text = neg_delta_hour_text + neg_delta_minute_text

    # Show planet's time (HH:MM)
    planet_time = (NOW - neg_delta).time()
    hours = planet_time.hour
    minutes = planet_time.minute
    if hours < 10:
        hours = f"0{hours}"
    if minutes < 10:
        minutes = f"0{minutes}"


    planetnavn = planet["navn"]
    print(f"{planetnavn} {hours}:{minutes} ({neg_delta_text})")


with solar_system_ephemeris.set("jpl"):
    for p in planets:
        get_planet_time(p)
    sun = get_sun(Time.now())
    print(sun.distance)
    # print(get_planet_time(sun))
