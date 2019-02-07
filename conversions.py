# Library for converting units

# Units
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


# Unit conversions

# Temperature
# NWS uses degrees C
def convert_NWS_temp(temp):
    if(imperial):
        return temp * (9/5) + 32
    else:
        return temp

# OWM returns data in Kelvin.
def convert_OWM_temp(kelvin):
    if(imperial):
        return kelvin * (9/5) - 459.67
    else:
        return kelvin - 273.15

# Pressure
# NWS uses pascal, so conversion to both inches of mercury and mbar are needed
def convert_NWS_pressure(press):
    if(imperial):
        return press / 3386.389
    else:
        return press / 100

# OWM uses mbar in their data
def convert_OWM_pressure(mbar):
    if(imperial):
        return mbar / 33.864
    else:
        return mbar

# Wind Speed is given in meters/second from both sources, convert to MPH or KPH
def convert_speed(ms):
    if(imperial):
        return ms * 2.237
    else:
        return ms * 3.6
