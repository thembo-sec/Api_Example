import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["API"]["KEY"]

# URLS
BASE_URL = "https://www.virustotal.com/api/v3/"
IP_URL = f"{BASE_URL}/ip_addresses"
DOMAIN_URL = f"{BASE_URL}/domains"
FILE_URL = f"{BASE_URL}/files"


class VirusTotal:
    def __init__(self, api_key: str = API_KEY) -> None:
        # damn look it remembers its own attribute thats 🔥, classes fucking rock
        self.headers = {"x-apikey": api_key}

    def get_ip(self, ip: str) -> dict:
        """Gets the VT response for a given IP"""
        url = f"{IP_URL}/{ip}"
        request = requests.get(url, headers=self.headers)

        return request.json()

    def get_domain(self, domain: str) -> dict:
        """Gets the VT response for a given domain"""
        url = f"{DOMAIN_URL}/{domain}"
        request = requests.get(url, headers=self.headers)

        return request.json()

    def get_file(self, hash: str) -> dict:
        """Gets the VT response for a given file hash"""
        url = f"{FILE_URL}/{hash}"
        request = requests.get(url, headers=self.headers)

        return request.json()


if __name__ == "__main__":
    vt = VirusTotal()
    ip = vt.get_ip("1.1.1.1")
    domain = vt.get_domain("facebook.com")
    # I'll buy a beverage of choice for the first person who recognises this hash
    file = vt.get_file("f3df1be26cc7cbd8252ab5632b62d740")
    print(file)
