# import urllib.parse
# import urllib.request
import requests
import json
from api_key import API_KEY

GET_DATA = True
BASE_URL = "https://api.izi.travel/"

def main():
    country_filename = "countries.json"
    museum_filename = "museum.json"

    if GET_DATA:
        country_cache(country_filename, limit=300)
        country_file = open_cache(country_filename)
        get_museum(country_file, museum_filename)

    museum_file = open_cache(museum_filename)
    print(len(museum_file["museums"]))



def country_cache(filename, offset=0, limit=1):
    url = "https://api.izi.travel/countries"
    params = {"api_key": API_KEY, "languages":"en", "offset": offset, "limit": limit}
    response = requests.get(url, params=params)

    print("Writing to file...")
    cache_dict = {"countries": response.json()}
    save_cache(cache_dict, filename=filename)
    
def get_museum(country_file, museum_file):
    country_dic = country_file["countries"]
    museum_list = []
    for i in range(len(country_dic)):
        UUID = country_dic[i]["uuid"]
        url = "https://api.izi.travel/countries/" + UUID + "/children"
        params = {"api_key": API_KEY, "languages":"en", "limit": 700}
        response = requests.get(url, params=params)
        results = response.json()
        for j in range(len(results)):
            if results[j].get("type") == "museum":
                museum_list.append(results[j])

    museum_cache = {"museums": museum_list}
    save_cache(museum_cache, filename=museum_file)



def open_cache(filename):
    """opens the cache file if it exists and loads the JSON into
    the FIB_CACHE dictionary.

    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache
    """
    try:
        cache_file = open(filename, "r")
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, filename):
    """saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    """
    dumped_json_cache = json.dumps(cache_dict, sort_keys=True, indent=2)
    fw = open(filename, "w")
    fw.write(dumped_json_cache)
    fw.close()


if __name__ == "__main__":
    main()