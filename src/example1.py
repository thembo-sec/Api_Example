import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["API"]["KEY"]

if __name__ == "__main__":

    headers = {"x-apikey": API_KEY}

    # babys first request 🥺
    request = requests.get(
        "https://www.virustotal.com/api/v3/ip_addresses/1.1.1.1", headers=headers
    )

    print(json.dumps(request.json(), indent=2))
