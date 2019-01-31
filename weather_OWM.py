# A simple, "pull forecast from the national weather service" program.

import json
import requests
import sys

# API key for the OpenWeatherMap website.
owm_api = "941419e458ad22c7d04828d09d3f1666"

# Unit dictionaries
imp_units = dict(zip(["temp", "wind", "pressure"], ["F", "MPH", "inHg"]))
metric_units = dict(zip(["temp", "wind", "pressure"], ["C", "KPH", "mBar"]))

# Default to imperial units
imperial = bool(1)
units = imp_units

# Lookup table for wind direction
wind = dict(zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West",
        "Northwest"]))


# API call function, returns the JSON
def get_json(url):
    request = requests.get(url)

    return json.loads(request.text)

def convert_temp(kelvin):
    if(imperial):
        return kelvin * (9/5) - 459.67
    else:
        return kelvin - 273.15

def convert_pressure(mbar):
    if(imperial):
        return mbar / 33.864
    else:
        return mbar

# Wind Speed is given in meters/second, convert to MPH or KPH
def convert_speed(ms):
    if(imperial):
        return ms * 2.237
    else:
        return ms * 3.6


# Get the lat/long of the passed in zip, then pass it to the NWS API for the
# purposes of getting their stored location data of the zip.
def get_point_info(lat, lon):
    return get_json("http://api.weather.gov/points/%f,%f" % (lat,lon))


# Display alerts for the area.
def display_alerts(alerts):
    alert_count = len(alerts)
    if alert_count == 0:
        print("No alerts for the area.\n\n")
        return

    for x in range(0,alert_count):
        print("Alert #%i\n" % (x + 1))
        print("%s\n\n%s\n\n%s\n\n" % (alerts[x]["properties"]["headline"],
            alerts[x]["properties"]["description"],
            alerts[x]["properties"]["instruction"]))

    return

# Display the current weather
def display_current(weather):
    print("Currently: %s" % weather["weather"][0]["description"])
    print("Temperature: %f %s" % (convert_temp(weather["main"]["temp"]), units["temp"]))
    print("Humidity: %i%%" % weather["main"]["humidity"])
    print("Pressure: %f %s" % (convert_pressure(weather["main"]["pressure"]), units["pressure"]))
    print("Wind %f %s @ %i\n\n" % (convert_speed(weather["wind"]["speed"]), units["wind"], weather["wind"]["deg"]))
    #calculate wind chill and heat index
    return

# Take in a forecast json dictionary from the NWS, then output it
def display_forecast(forecast):
    temp_type = ""
    periods = len(forecast["properties"]["periods"])

    for x in range(0, periods):
        data = forecast["properties"]["periods"][x]

        print("%s:" % data["name"])
        print(data["shortForecast"])

        if(data["isDaytime"]):
            temp_type = "High:"
        else:
            temp_type = "Low:" 

        if(data["temperatureTrend"]):
            print("%s %i %s and %s" % (temp_type, data["temperature"],
                data["temperatureUnit"], data["temperatureTrend"]))
        else:
            print("%s %i %s" % (temp_type, data["temperature"], data["temperatureUnit"]))

        print("Wind: %s at %s" % (wind[data["windDirection"]], data["windSpeed"]))
        print("Details: %s\n\n" % data["detailedForecast"])


#TODO functionize this?
# Currently hardcoded to home, pass this in from the command line eventually
# Get the current weather for the passed in zip code
#currently hardcoded to Milwaukee, WI
current_w = get_json("https://api.openweathermap.org/data/2.5/weather?zip=%i,us&APPID=%s" % (53263, owm_api))

# Display the current weather
display_current(current_w)

# extract the latitude and longitude from the json.  This will be used to pull
# the current weather alerts from the National Weather Service.
lat = current_w["coord"]["lat"]
lon = current_w["coord"]["lon"]

local = get_json("http://api.weather.gov/points/%f,%f" % (lat,lon))

# Pull the forecast api URL from the local data.  This will then be used to grab
# the actual forecast
forecast_api = local["properties"]["forecast"]

# Grab the forecast from the NWS
display_forecast(get_json(forecast_api))

# Pull the forecast zone API URL from the local data.  This will be used for
# getting the alerts for the given area
fzone_api = local["properties"]["forecastZone"]

# Grab the zone id
zone_info = get_json(fzone_api)

zone_id = zone_info["properties"]["id"]

# Get the alerts for the area
alerts = get_json("https://api.weather.gov/alerts/active/zone/%s" % zone_id)

display_alerts(alerts["features"])

