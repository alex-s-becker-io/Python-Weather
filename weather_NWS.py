# A simple, "pull forecast from the national weather service" program.

import json
import requests
import sys

#API key for the zipcodeapi website.
zip_api = "g4L4gd4sOfNOFv9g0E5XfVA5pDPdmOMKyxMgZR9r9G4cNYyhOt0pZ4dxks5Tcic1"

# Lookup table for wind direction
wind = dict(zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West",
        "Northwest"]))

# Query the zipcodeapi database for the latitude and longitude of the given zip 
# code.  This data is needed properly query the NWS API.
#
# LIMITED TO TEN REQUESTS PER HOUR
def get_lat_long(zip_code):
    location_request = requests.get("https://www.zipcodeapi.com/rest/%s/info.json/%s/degrees" % (zip_api, zip_code))
    location_json = json.loads(location_request.text)

    return str(location_json["lat"]) + "," + str(location_json["lng"])

# Get the lat/long of the passed in zip, then pass it to the NWS API for the
# purposes of getting their stored location data of the zip.
def get_point_info(zip_code):
    point_info = requests.get("http://api.weather.gov/points/%s" % get_lat_long(zip_code))

    return json.loads(point_info.text)

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
# Currently hardcoded to Milwaukee, pass this in from the command line eventually
local = get_point_info("53263")

# Pull the forecast zone API URL from the local data.  This will be used for
# getting the alerts for the given area
fzone_api = local["properties"]["forecastZone"]

# Pull the forecast api URL from the local data.  This will then be used to grab
# the actual forecast
forecast_api = local["properties"]["forecast"]

# Grab the forecast from the NWS
r_forecast = requests.get(forecast_api)
forecast = json.loads(r_forecast.text)

display_forecast(forecast)

# Grab the zone id
r_zone_info = requests.get(fzone_api)
zone_info = json.loads(r_zone_info.text)

zone_id = zone_info["properties"]["id"]

# Get the alerts for the area
r_alerts = requests.get("https://api.weather.gov/alerts/active/zone/%s" % zone_id)
alerts = json.loads(r_alerts.text)

display_alerts(alerts["features"])
