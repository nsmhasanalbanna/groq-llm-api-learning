import requests
from config.settings import settings

def get_geofy_client(area_name):
    url = "https://api.geoapify.com/v1/geocode/search"
    headers = {"Accept" : "application/json"}
    params = {
        "text" : area_name,
        "apiKey" : settings.geo_api_key
    }
    geo_response = requests.get(url,headers=headers,params=params)
    return geo_response