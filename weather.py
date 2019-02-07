# Weather reporting script
# The purpose of this script is to pull data from the National Weather Service.
#
# The data pulled from the NWS includes:
# -current observations (from the nearest METAR station)
# -forecast (either as a point or a zone, depending)
# -Alerts for the given area
#
# OpenWeatherMaps (OWM) is used to convert the passed in Zip Code to lat/lon
# coordinates, as the NWS's APIs are not able to do so at the moment.  Also
# note that the NWS APIs are considered experimental except for the alerts API,
# which means they can fail at any time (and will).
#
# Current functionality is to simply read the forecast data and alerts.
#
# Planned functionality:
# -Current observations from nearest METAR station
# -imperial/metric units (current: imperial only)
# -International forecasting via OWM.
# -Potenially pulling products from the Storm Prediction Center

# Imports
import json
import requests
import sys
import conversions
import NWS

# API key for the OpenWeatherMap website.
owm_api = "941419e458ad22c7d04828d09d3f1666"

# Data source
NWS_data = True  # default to NWS

# API call function, returns the JSON
def get_json(url):
    request = requests.get(url)
    return json.loads(request.text)


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

# Read in location from command line
#TODO actually implement this.  Right now current zip being used is for Butler, WI
current_w = get_json("https://api.openweathermap.org/data/2.5/weather?zip=%i,us&APPID=%s" % (53263, owm_api))

# Extract the latitude and longitude from the json.  This will be used to pull
# the current weather alerts from the National Weather Service.
lat = current_w["coord"]["lat"]
lon = current_w["coord"]["lon"]

local = get_json("http://api.weather.gov/points/%f,%f" % (lat,lon))

city = local["properties"]["relativeLocation"]["properties"]["city"]
state = local["properties"]["relativeLocation"]["properties"]["state"]

print("Forecast for %s, %s\n\n" % (city, state))

# Pull the forecast zone API URL from the local data.  This will be used for
# getting the alerts for the given area
fzone_api = local["properties"]["forecastZone"]

# Grab the zone id
zone_info = get_json(fzone_api)

zone_id = zone_info["properties"]["id"]

# Pull the forecast api URL from the local data.  This will then be used to grab
# the actual forecast
forecast_api = local["properties"]["forecast"]

# Grab the forecast from the NWS
success = NWS.display_forecast(get_json(forecast_api), "point")
if not success:
    print("Unable to retreive the point forecast for the given area, using the zone forecast")
    success = NWS.display_forecast(get_json("https://api.weather.gov/zones/forecast/%s/forecast" % zone_id), "zone")
    if not success:
        print("Unable to retrieve the zone forecast for the given area.")



# Get the alerts for the area
alerts = get_json("https://api.weather.gov/alerts/active/zone/%s" % zone_id)

NWS.display_alerts(alerts["features"])
