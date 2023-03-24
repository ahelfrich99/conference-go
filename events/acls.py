from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests

def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    params = {"per_page": 1, "query": city + " " + state}
    headers = {"authorization": PEXELS_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)

    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}

def get_weather_data(city, state):
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    geocoding = requests.get(geocoding_url, params=params)
    geo_content = json.loads(geocoding.content)
    print(geo_content)

    try:
        lat = geo_content[0]["lat"]
        lon = geo_content[0]["lon"]
    except (KeyError, IndexError):
        return None


    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    weather = requests.get(weather_url, params=params)
    weather_content = json.loads(weather.content)

    try:
        return {
            "temp": weather_content["main"]["temp"],
            "description": weather_content["weather"][0]["description"],
        }
    except (KeyError, IndexError):
        return None

print(get_weather_data("Philadelphia", "PA")
)
'''
- start by looking at the documentation
    - the url under the example request
    - the query is going to be a city and state
    - number of results per page is 1 for us, default is 15
- acls.py
    - define the function, pass in city and state
    - define url = https://api.pexels.com/v1/search
    - define params = {"per_page": 1, "query": city + " " + state}
    - define headers = dict including authorization: PexelsAPIKEY
    - response = requests.get(url, params=params, headers=headers)
    - content = json.loads(response.content)
    - try return {"picture_url": content["photos"][0]["src"]["original"]}
    - execpt if key error or index error
        return {"picture_url": None}
- api_views
    - go into list_locations
    - call get_photo function with the content city and state.abbreviation
        - and set that equal to photo
    - update the content so that it has the photo in it
- LocationDetailEncoder
    - add picture_url to the list of properties
'''
