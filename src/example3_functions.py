import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["API"]["KEY"]
BASE_URL = "https://www.virustotal.com/api/v3/"


def get_ip(ip: str) -> dict:
    """Gets the VT response for a given IP

    Args:
        ip (str): The IP in question
    """
    headers = {"x-apikey": API_KEY}
    ip_url = f"{BASE_URL}/ip_addresses/{ip}"
    ip_request = requests.get(ip_url, headers=headers)

    return ip_request.json()


if __name__ == "__main__":

    # Holy fucking bingle, abstraction!
    ip1 = get_ip("1.1.1.1")

    # Damn I can get IP's all day like this!
    ip2 = get_ip("8.8.8.8")

    # I can barely hold all the DNS's
    ip3 = get_ip("9.9.9.9")

    # Even the same one twice!
    ip4 = get_ip("9.9.9.9")

    # VT party over, hit the request limit (VT is 4 per/min)
    ip5 = get_ip("9.9.9.9")
