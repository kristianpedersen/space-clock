import datetime
import pytz

from astropy import units as u
from astropy.coordinates import get_body, get_sun
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.time import Time, TimeDelta
from flask import Flask, send_from_directory

app = Flask(__name__)


def add_leading_zero(number):
    if number < 10:
        return f"0{number}"
    return f"{number}"


LIGHT_MINUTE = (1 * u.year).to(u.minute).value
LIGHT_DAY = (1 * u.year).to(u.day).value

time_string = Time.now().to_datetime(timezone=pytz.timezone("Europe/Oslo"))
time_string = str(time_string).split(".")[0]
current_time = Time(time_string)
observation_location = EarthLocation.from_geodetic(60.79574, 10.69155)

current_year = current_time.to_datetime().year
current_time_hour = add_leading_zero(current_time.to_datetime().hour)
current_time_minute = add_leading_zero(current_time.to_datetime().minute)
current_time_formatted = f"{current_time_hour}:{current_time_minute}"

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

# extrasolar_objects = [
#     {"name": "Proxima Centauri", "distance": "litt over 4 år", "info": "den nærmeste stjerna utenom sola"},
#     {"name": "Sirius", "distance": "8½ år", "info": "den mest lyssterke stjerna på nattehimmelen"},
#     {"name": "TRAPPIST-planetene", "distance": "ca. 39 år", "info": "et planetsystem med en jordlignende planet"},
#     {"name": "Alkaid", "distance": "104 år", "info": },
#     {"name": "Polaris", "distance": "323 år"},
# ]

final_output = []


def get_star_date(ly):
    body_distance_light_days = (
        (ly * u.lightyear).to(u.lightyear) * LIGHT_DAY).value
    time_delta = TimeDelta(body_distance_light_days)
    observed_time = current_time - time_delta
    return observed_time


def get_body_time(body, name):
    # Get distance in light days, because that's how AstroPy's TimeDelta function works
    body_distance_light_days = (
        body.distance.to(u.lightyear) * LIGHT_DAY).value
    time_delta = TimeDelta(body_distance_light_days)
    observed_time = current_time - time_delta

    hour = add_leading_zero(observed_time.to_datetime().hour)
    minute = add_leading_zero(observed_time.to_datetime().minute)

    time_difference = (current_time - observed_time).to_datetime()
    time_difference_hours = int(str(time_difference).split(":")[0])
    time_difference_minutes = int(str(time_difference).split(":")[1])

    # We want a string that says "x hour(s) and y minute(s) ago"
    time_difference_string = ""

    if time_difference_hours == 1:
        time_difference_string = "1 time og "
    elif time_difference_hours > 1:
        time_difference_string = f"{time_difference_hours} timer og "

    if time_difference_minutes == 1:
        time_difference_string += "1 minutt"
    elif time_difference_minutes > 1:
        time_difference_string += f"{time_difference_minutes} minutter"

    if name == "Mercury":
        name = "Merkur"
    if name == "Neptune":
        name = "Neptun"

    final_output.append({
        "name": name,
        "time": f"{hour}:{minute}",
        "delta": time_difference_string
    })


with solar_system_ephemeris.set("jpl"):
    sun = get_sun(current_time)
    get_body_time(sun, "Sola")

    for planet_name in planets:
        planet = get_body(planet_name, current_time, observation_location)
        get_body_time(planet, planet_name)

# for body in extrasolar_objects:
#     final_output.append({
#         "name": body["name"],
#         "delta": body["distance"]
#     })


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
    app.run(debug=True)
