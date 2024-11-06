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


# Make a child class of a request Session. Comes with all this handy functionality
# some smarter person has already implemented!
class VirusTotal(requests.Session):
    """Class used to interact with the VT API

    Args:
        api_key (str, optional): Api key for interacting the the server. Defaults to API_KEY.
        base_url (str, optional): Base url of the server. Defaults to BASE_URL.
        ssl_verification (bool, optional): Turn SSL verification on/off. Defaults to True.
    """

    def __init__(
        self,
        api_key: str = API_KEY,
        base_url: str = BASE_URL,
        ssl_verification: bool = True,
    ) -> None:

        super().__init__()
        self.headers.update({"x-apikey": api_key})
        self.verify = ssl_verification
        self.base_url = base_url
        self._create_endpoints()

    def __getattr__(self, name):
        endpoint = Endpoint(name, self)
        self.__setattr__(name, Endpoint(name, self))
        # return it so it can be instantiated AND called at the same time
        return endpoint

    def _create_endpoints(self):
        """
        Create a set of existing endpoints
        """
        logger.debug("Creating existing endpoints")
        self.ip_addresses = Endpoint("ip_addresses", session=self, methods=["GET"])

    def get_ip_addr(self, ip: str) -> dict:
        """Get IP address.

        Serves as a wrapper for the ip_addresses endpoint.

        Args:
            ip (str): Ip address to get info for.

        Returns:
            dict: Info on IP address
        """
        return self.ip_addresses(ip).json()


class Endpoint:
    """Endpoint class used for calling endpoints

    Args:
        name (str): Endpoint name, used for building the url
        session (VirusTotal): Requests session child class used for any requests
        methods (list, optional): Methods that are available at this endpoint. Defaults to `["GET"]`.
        required (dict, optional): Required parameters for a given method.
            Done in the format: `{"GET": ["param1", "param2"]}`. Defaults to `{}`.
    """

    def __init__(
        self,
        name: str,
        session: VirusTotal,
        methods: list = None,
        required: dict = {},
    ):
        self.name = name
        self.session = session
        self.methods = methods
        self.required = required

    def __call__(self, *args, **kwargs) -> requests.Response:
        """
        I should call them...
        """
        method = self._validate_method(kwargs.pop("method", "GET"))

        self._check_required(params=kwargs, method=method)
        
        data = kwargs.pop("data", None)

        if len(args) > 0:
            url = f"{BASE_URL}{self.name}/{args[0]}"
        else:
            url = f"{BASE_URL}{self.name}"

        try:
            response = self.session.request(
                method=method, url=url, params=kwargs, data=data
            )
            return self._response_handler(response).json()

        except Exception as err:
            logger.exception(err)

    def _validate_method(self, method: str) -> str:
        """Ensure the method being used in the request is available on that endpoint.

        Args:
            method (str): Method being called

        Raises:
            requests.exceptions.HTTPError: Method not available at this endpoint

        Returns:
            str: The method being called.
        """

        if self.methods is not None:
            if method not in self.methods:
                raise requests.exceptions.HTTPError(
                    "Method not available on this endpoint. Available methods: {}".format(
                        self.methods
                    )
                )
        return method

    def _check_required(self, method: str, params: dict = None) -> dict:
        """Checks if the request contains any missing parameters

        Args:
            params (dict): Request parameters.
            method (str): Request method.

        Raises:
            KeyError: Missing required parameters

        Returns:
            dict: parameter dictionary
        """
        for parameter in self.required.get(method, []):
            if not params:
                raise KeyError(
                    f"Query missing required parameters. Required: {self.required.get(method)}"
                )

            if params.get(parameter, None) is None:
                raise KeyError(
                    f"Query missing required parameters. Given: {params}. Required: {self.required.get(method)}"
                )

        return params

    def _response_handler(self, response: requests.Response) -> requests.Response:
        """Some kind of handler for response errors.

        Args:
            response (requests.Response): Response from the server

        Returns:
            requests.Response: Response from the server.
        """
        match response.status_code:
            case 200:
                return response
            case _:
                logger.error(
                    f"Response error: {response.status_code}. Details: {response.text}. Url: {response.url}"
                )
                return response


if __name__ == "__main__":
    vt = VirusTotal()
    logger.info("Test")

    # create it, call it and grab the data all here
    # search = vt.file(query="f3df1be26cc7cbd8252ab5632b62d740")
    ip = vt.ip_addresses("103.45.69.117", method='POST')

    print(json.dumps(ip, indent=2))
    # print(json.dumps(ip, indent=2))
