# Require the httparty gem


# Set up the url and send a GET request to it. The base url is:
# "https://api.nasa.gov/planetary/apod?api_key=NNKOjkoul8n1CH18TWA9gwngW1s1SmjESPjNoUFo"

# https://api.nasa.gov/planetary/apod?api_key=xS3hW6yhSnUuJjGThfAJVO2DvD9Gra3M2DcPe4Sq

# Make the request and print out the "url" key in the response, which is the image url

# importing the requests library
import requests

# api-endpoint
URL = "https://api.nasa.gov/planetary/apod"

# location given here
birthday = "1995-08-14"
key = "xS3hW6yhSnUuJjGThfAJVO2DvD9Gra3M2DcPe4Sq"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'date':birthday, 'api_key': key}

# sending get request and saving the response as response object
r = requests.get(url = URL, params=PARAMS)

data = r.json()

print(data['url'])
