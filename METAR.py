# METAR parsing
test_mke = "KMKE 080352Z 26021G40KT 9SM -SN BKN020 M10/M15 A2983 RMK AO2 PK WND 25040/0349 SLP112 P0000 T11001150 $"
test_pdx = "KPDX 080353Z 12010KT 10SM SCT140 OVC250 M01/M07 A3028 RMK AO2 SLP254 T10061072"

# Length of the direction string
DIRECTION_END   = 3

# Parse the wind data.
#
# Wind data will always be laid out in the following: dddssGggKT
#   ddd = wind direction
#   ss  = sustained speed in knots.  Can be 3 digits
#   G   = presence of gusts.  Won't always be included
#   gg  = gust speed in knots.  Can be 3 digits
#   KT  = Units
#
#TODO Will need to handle international METAR
def parse_wind(wind):
    # Check for calm winds.  This is always "00000KT".
    #TODO international units
    if wind == "00000KT":
        print("Calm winds")
        return

    # Get the direction string.  This is always the first three characters of
    # the wind string.
    direction = wind[0:DIRECTION_END]

    if direction == "VRB":
        print("Variable Winds")
    else:
        # make helper function here to calculate direction
        print("Winds out of the %s" % direction)

    # We want to start at the first character after the direction
    x = DIRECTION_END
    sustained = ""

    # Loop until we hit a letter, which will indicate the end of the sustained
    # wind data
    while wind[x].isdigit():
        sustained += wind[x]
        x += 1
    print("Wind Speed: %i" % int(sustained))

    # Check for gusts.  This is indicated by a G after the sustained wind info.
    if wind[x] == 'G':
        # Move past the Gust indicator
        x += 1
        gust = ""

        # Loop until we hit the unit indicator
        while wind[x].isdigit():
            gust += wind[x]
            x += 1

        print("Wind Gusts: %i" % int(gust))

    return

# METAR RULES:
# Airport Code
# time, zulu
# wind
# -wind variablity
# visiblity
# -weather condition
# sky condition
# temperature/dewpoint
# pressure
# remarks
def parse_metar(data):
    x = 0;

    # First token can be METAR, SPECI, or blank.  This tells us whether or not
    # it was an hourly or mid-hour request
    # Handle METAR case
    if data[x] == "METAR":
        print("Hourly observation at %s" % data[x + 1])
        x += 1 # Skip the next token, as it's used to show where the data is from
    # Handle SPECI case
    elif data[x] == "SPECI":
        print("Special observation at %s" % data[x + 1])
        x += 1 # Skip the next token, as it's used to show where the data is from
    # Handle blank
    else: 
        print("Observations at %s" % data[x])

    x += 1

    # Next token will always be the time and date
    #TODO convert to more "human readable" format
    print("Observation taken at %s" % data[x])
    x += 1

    # Occasionally there will be extra data between the date and time and the
    # wind speed.  This data indicates whether or not it was an automatic
    # recording (AUTO) or a correction to a previous observation.  We're not
    # interested in this data, so move past it.  The next token we are
    # interested in is the wind information, which ends in KT, KMH, or MPS,
    # depending on the country of origin.
    while not data[x].endswith(("KT","KMH","MPS")):
        x += 1

    # Parse the wind data
    parse_wind(data[x])
    x += 1

    # Check to if the wind is varying.  This is indicated by a V in the string
    # right after the primary wind data string
    #
    # Format: xxxVyyy
    #   xxx - Degree X
    #   V   - variable wind indicator
    #   yyy - Degree Y
    # This means the winds are varying between X and Y for direction.  It will
    # only appear if there is a 60 degree difference
    if 'V' in data[x]:
        print("Winds varying between %s and %s" % (data[x][0:3], data[x][4,7]))
        x += 1
    
    # Next data set is the visibility.  The units are statute miles in the US
    # and Canada, meters elsewhere.  Unfortunately, it is impossible to directly
    # convert to an integer or float, as it can (and will) be expressed in
    # fractions.  That handling will come in time.
    #
    # Format: xxxxSM
    #   xxxx    - Distance
    #   SM      - Units
    vis = ''
    y = 0
    while data[x][y] != 'S':
        vis += data[x][y]
        y += 1

    print("Visibility: %s miles" % vis)
    x += 1

    # Discard runway information.  This is prefaced with an R and is between the
    # visibility and current weather status.  We're not interested in it at the
    # moment.  This functionality will come later, but for now ignore.
    while data[x][0] == 'R':
        x += 1
 
    # Dump the rest of the data until the parser is set up for it
    while x < len(data):
        print("Token #%i: %s" % (x, data[x]))
        x += 1

    return 

mke_metar_data = test_mke.split(' ')

visiblity_last = False

parse_metar(mke_metar_data)
