import configparser
import json
import logging.config
import requests
import logging

config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")
API_KEY = config["API"]["KEY"]
LOG_FMT = config["LOG"]["fmt"]

logger = logging.getLogger(__name__)
logging.basicConfig(format=LOG_FMT, level=0, datefmt="%Y/%m/%d %I:%M:%S")

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

    def __getattr__(self, name):
        endpoint = Endpoint(name, self)
        self.__setattr__(name, Endpoint(name, self))
        # return it so it can be instantiated AND called at the same time
        return endpoint


class Endpoint:
    def __init__(self, name, session: VirusTotal):
        self.name = name
        self.session = session
        logger.info(f"Creating endpoint: {name}")

    def __call__(self):
        """
        Doing something!
        """
        logger.info("Calling myself")
        print(f"{self.__repr__()} | {self.__dict__}")


if __name__ == "__main__":
    vt = VirusTotal()
    logger.info("Test")
    #  this shouldn't work, this attribute doesn't exist!
    vt.popular_threat_categories

    vt.popular_threat_categories()
    # I can instantiate and call at the same time?

    vt.domains()
    vt.files()
    # 🦀 and C programers screaming and crying, they'd need at least 10k lines for this
