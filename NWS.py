# Lookup table for wind direction
wind = dict(zip(["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West",
        "Northwest"]))

def display_point_forecast(forecast):
    # Will be used if temperature is rising or falling
    temp_type = ""

    # Get the number of periods in the forecast
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

    return True


def display_zone_forecast(forecast):
    periods = len(forecast["periods"])

    for x in range(0, periods):
        data = forecast["periods"][x]

        print("%s:" % data["name"])
        print("Details: %s\n" % data["detailedForecast"])

    return True


def display_forecast(forecast, f_type):
    # Occasionally the NWS API can't find the data internally and will not
    # return the values.  We want to exit early if this is the case.
    if("status" in forecast):
        return False

    # Point and Zone forecasts have two different data sets, so process them
    # differently
    if f_type == "point":
        return display_point_forecast(forecast)
    elif f_type == "zone":
        return display_zone_forecast(forecast)
    else:
        return False


# Display alerts for the area.
def display_alerts(alerts):
    # See how many alerts we have
    alert_count = len(alerts)

    # If none exist, simply state so and exit
    if alert_count == 0:
        print("No alerts for the area.\n\n")
        return None

    for x in range(0,alert_count):
        print("Alert #%i\n" % (x + 1))
        print("%s\n\n%s\n\n%s\n\n" % (alerts[x]["properties"]["headline"],
            alerts[x]["properties"]["description"],
            alerts[x]["properties"]["instruction"]))

    return None
