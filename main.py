import datetime
import pytz

from astropy import units as u
from astropy.coordinates import get_body, get_sun
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.time import Time, TimeDelta
from flask import Flask, send_from_directory

app = Flask(__name__)

LIGHT_MINUTE = (1 * u.year).to(u.minute).value
LIGHT_DAY = (1 * u.year).to(u.day).value

time_string = Time.now().to_datetime(timezone=pytz.timezone("Europe/Oslo"))
time_string = str(time_string).split(".")[0]
current_time = Time(time_string)
observation_location = EarthLocation.from_geodetic(60.79574, 10.69155)

planets = [
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",  # It's not a planet, but everyone loves Pluto
]

final_output = []


def add_leading_zero(number):
    if number < 10:
        return f"0{number}"
    return f"{number}"


def get_body_time(body, name):
    # Get distance in light days, because that's how AstroPy's TimeDelta function works
    body_distance_light_days = (
        body.distance.to(u.lightyear) * LIGHT_DAY).value
    time_delta = TimeDelta(body_distance_light_days)
    observed_time = current_time - time_delta

    time_difference = (current_time - observed_time).to_datetime()
    time_difference_hours = int(str(time_difference).split(":")[0])
    time_difference_minutes = int(str(time_difference).split(":")[1])

    time_difference_string = ""

    if time_difference_hours == 1:
        time_difference_string = "1 hour and "
    elif time_difference_hours > 1:
        time_difference_string = f"{time_difference_hours} hours and "

    if time_difference_minutes == 1:
        time_difference_string += "1 minute"
    elif time_difference_minutes > 1:
        time_difference_string += f"{time_difference_minutes} minutes"

    final_output.append({
        "name": name,
        "delta": time_difference_string
    })


with solar_system_ephemeris.set("jpl"):
    sun = get_sun(current_time)
    get_body_time(sun, "the sun")

    for planet_name in planets:
        planet = get_body(planet_name, current_time, observation_location)
        get_body_time(planet, planet_name)

final_output.append({"name": "Sirius", "delta": "8½ years"})
final_output.append({"name": "Polaris", "delta": "323 years"})
final_output.append(
    {"name": "The biggest black hole (M83)", "delta": "53.5 million years"})
print(final_output)


@app.route("/")
def hello():
    return send_from_directory("client/public", "index.html")


@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


@app.route("/get-body-info")
def get_planet_info():
    return str(final_output)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
