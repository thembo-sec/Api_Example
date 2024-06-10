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

    def __call__(self, *args, **kwargs):
        """
        I should call them...
        """
        method = kwargs.pop("method", "GET")
        if len(args) > 0:
            url = f"{BASE_URL}{self.name}/{args[0]}"
        else:
            url = f"{BASE_URL}{self.name}"

        try:
            response = self.session.request(method=method, url=url, params=kwargs)
            return response.json()

        except Exception as err:
            logger.exception(err)


if __name__ == "__main__":
    vt = VirusTotal()
    logger.info("Test")

    # create it, call it and grab the data all here
    search = vt.search(query="f3df1be26cc7cbd8252ab5632b62d740")
    # ip = vt.ip_addresses("9.9.9.9")

    print(json.dumps(search, indent=2))
    # print(json.dumps(ip, indent=2))
