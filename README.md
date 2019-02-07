# Python-Weather

A simple script to pull weather data off of the National Weather Service (NWS) API.  The API itself is a bit touchy, and prone to 404'ing, but it provides some robust information, as well as major alerts for a given area.  Open Weather Map (OWM) is also used to source some information, particularly the latitude and longitude of a given zip code.

The \_NWS file pulls solely from the NWS, except for a call to ZipCodeApi.com.  ZipCodeApi has a rate limit of 10 calls an hour, so it's not preferred.  The \_OWM file calls OWM with a zip code to get the lat/long data, which is then fed to the NWS for data.

The current plan is to move the NWS functions into its own file, and have how the lat/long data be parsed in two different ways from the command line.

The `requests` library is used, and can be acquired from here: http://docs.python-requests.org/en/master/
