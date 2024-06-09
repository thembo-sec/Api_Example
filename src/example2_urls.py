import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["API"]["KEY"]
BASE_URL = "https://www.virustotal.com/api/v3/"

if __name__ == "__main__":
    headers = {"x-apikey": API_KEY}

    # Oooft, look how much less typing i've done 😎
    ip_url = f"{BASE_URL}/ip_addresses/1.1.1.1"
    ip2_url = f"{BASE_URL}/ip_addresses/8.8.8.8"

    ip_request = requests.get(ip_url, headers=headers)
    ip2_request = requests.get(ip2_url, headers=headers)

    # Do something fun with the responses. Print them to the terminal in JSON!
    # Thats fun!
    print(json.dumps(ip_request.json(), indent=2))
    print(json.dumps(ip2_request.json(), indent=2))
