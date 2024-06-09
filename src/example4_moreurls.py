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


def get_ip(ip: str) -> dict:
    """Gets the VT response for a given IP

    Args:
        ip (str): The IP in question
    """
    headers = {"x-apikey": API_KEY}
    url = f"{IP_URL}/{ip}"
    request = requests.get(url, headers=headers)

    return request.json()


def get_domain(domain: str) -> dict:
    """Gets the VT response for a given domain

    Args:
        domain (str): The domain in question
    """
    headers = {"x-apikey": API_KEY}
    url = f"{BASE_URL}/{domain}"
    request = requests.get(url, headers=headers)

    return request.json()


def get_file(hash: str) -> dict:
    """Gets the VT response for a given file hash

    Args:
        hash (str): SHA-256, SHA-1 or MD5 identifying the file
    """
    headers = {"x-apikey": API_KEY}
    url = f"{FILE_URL}/{hash}"
    request = requests.get(url, headers=headers)

    return request.json()


if __name__ == "__main__":
    # Damn look at all these functions dawg, so much easier
    ip = get_ip("1.1.1.1")
    domain = get_domain("facebook.com")
    # I'll buy a beverage of choice for the first person who recognises this hash
    file = get_file("f3df1be26cc7cbd8252ab5632b62d740")
