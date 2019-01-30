# A simple, "pull forecast from the national weather service" program.

import json
import requests
import sys

#API key for the OpenWeatherMap website.
owm_api = "941419e458ad22c7d04828d09d3f1666"

# Lookup table for wind direction
wind = dict(zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West",
        "Northwest"]))


# API call function, returns the JSON
def get_json(url):
    request = requests.get(url)

    return json.loads(request.text)

def k_to_f(kelvin):
    return kelvin * (9/5) - 459.67

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
        print("Alert #" + str(x + 1) + "\n")
        print(alerts[x]["properties"]["headline"])
        print("\n")
        print(alerts[x]["properties"]["description"])
        print("\n")
        print(alerts[x]["properties"]["instruction"])
        print()
        print()

    return

def display_current(weather):
    print("Currently: %s" % weather["weather"][0]["description"])
    print("Temperature %f F" % k_to_f(weather["main"]["temp"]))
    print("Pressure %i hPa" % weather["main"]["pressure"])
    print("Wind %f @ %i" % (weather["wind"]["speed"], weather["wind"]["deg"]))
    #calculate wind chill
    return

# Take in a forecast json dictionary from the NWS, then output it
def display_forecast(forecast):
    temp_type = ""
    periods = len(forecast["properties"]["periods"])

    for x in range(0, periods):
        data = forecast["properties"]["periods"][x]

        print(data["name"] + ":")
        print(data["shortForecast"])

        if(data["isDaytime"]):
            temp_type = "High: "
        else:
            temp_type = "Low: " 

        if(data["temperatureTrend"]):
            print(temp_type + str(data["temperature"]) + " " +
                    data["temperatureUnit"] + " and " + data["temperatureTrend"])
        else:
            print(temp_type + str(data["temperature"]) + " " +
                    data["temperatureUnit"])

        print("Wind: " + wind[data["windDirection"]] + " at " + data["windSpeed"])
        print("Details: " + data["detailedForecast"])
        print()

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

# Pull the forecast zone API URL from the local data.  This will be used for
# getting the alerts for the given area
fzone_api = local["properties"]["forecastZone"]

# Grab the zone id
zone_info = get_json(fzone_api)

zone_id = zone_info["properties"]["id"]

# Get the alerts for the area
alerts = get_json("https://api.weather.gov/alerts/active/zone/%s" % zone_id)

display_alerts(alerts["features"])

# Pull the forecast api URL from the local data.  This will then be used to grab
# the actual forecast
#forecast_api = local["properties"]["forecast"]

# Grab the forecast from the NWS

#display_forecast(forecast)
