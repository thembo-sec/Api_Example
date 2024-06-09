import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["API"]["KEY"]
BASE_URL = "https://www.virustotal.com/api/v3/"

if __name__ == "__main__":
    headers = {"x-apikey": API_KEY}
    url = f"{BASE_URL}/ip_addresses/1.1.1.1"

    request = requests.get(url, headers=headers)
    print(json.dumps(request.json(), indent=2))
