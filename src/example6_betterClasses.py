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


# Make a child class of a request Session. Comes with all this handy functionality
# some smarter person has already implemented!
class VirusTotal(requests.Session):
    """Class used to interact with the VT API

    Args:
        api_key (str, optional): Defaults to API_KEY.
    """

    def __init__(self, api_key: str = API_KEY) -> None:
        # now we don't need to add those pesky headers every request
        super().__init__()
        self.headers.update({"x-apikey": api_key})

    def get_ip(self, ip: str) -> dict:
        """Gets the VT response for a given IP"""
        url = f"{IP_URL}/{ip}"
        request = self.get(url)

        return request.json()

    def get_domain(self, domain: str) -> dict:
        """Gets the VT response for a given domain"""
        url = f"{DOMAIN_URL}/{domain}"
        request = self.get(url)

        return request.json()

    def get_file(self, hash: str) -> dict:
        """Gets the VT response for a given file hash"""
        url = f"{FILE_URL}/{hash}"
        request = self.get(url)

        return request.json()


if __name__ == "__main__":
    vt = VirusTotal()
    ip = vt.get_ip("1.1.1.1")
    domain = vt.get_domain("facebook.com")
    # I'll buy a beverage of choice for the first person who recognises this hash
    file = vt.get_file("f3df1be26cc7cbd8252ab5632b62d740")
    print(json.dumps(file, indent=2))
