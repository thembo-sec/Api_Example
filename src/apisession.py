import requests

# TODO update this to VT API as I go
BASE_URL = "SOME_URL"


class ApiSession(requests.Session):
    """
    Session used for interacting with a rest API.

    Endpoints are created and called dynamically. Eg, an endpoint would be called:
    `ApiSession.endpoint(id=1)`

    Args:
        base_url (str): Base url for the API
        SSL_verification (bool): Use ssl verification
        access_token (str): Access token/api_key
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        ssl_verification: bool = True,
        access_token: str = None,
    ) -> None:
        """
        Dummy class that wraps a requests session.
        """

        super().__init__()
        self.base_url = base_url
        self.verify = ssl_verification
        self.headers.update({"Authorization": "Base {}".format(access_token)})
        self.create_endpoints()

    def __getattr__(self, name):
        """
        Called when an unknown attribute is attempted to be accessed
        """
        return Endpoint(name, self)

    def create_endpoints(self):
        """
        Create pre-existing endpoints, can be interacted with directly or via a
        wrapper method call. Useful for once prototyping is complete.
        """

        self.existing_endpoint = Endpoint(
            name="existing_endpoint",
            session=self,
            methods=["GET", "POST"],
            required={"GET": ["timestamp"]},
        )

    def call_existing_endpoint_wrapper(self, endpoint_args):
        """Wrapper method for the `existing_endpoint` child"""
        return self.existing_endpoint(endpoint_args)

    def _response_hander(self, response: requests.Response):
        match response.status_code:
            case 200:
                return response
            case _:
                print(
                    f"Error. Status: {response.status_code}. Details: {response.json()}"
                )


class Endpoint:
    def __init__(
        self, name, session: ApiSession, methods: list = None, required: dict = {}
    ) -> None:
        self.name = name
        self.session = session
        self.methods = methods
        self.required = required
        print(f"Creating endpoint at {session.base_url}/{self.name}")

    def __getattr__(self, name):
        return Endpoint("/".join([self.name, name]), self.session)

    def __call__(self, *args, **kwargs) -> requests.Response:
        """Called when an unknown method is called on itself"""
        print(f"Calling {self.name}")

        method = self._validate_method(kwargs.pop("method", "GET"))
        self.check_required(parameters=kwargs, method=method)
        data = kwargs.pop("data", None)

        # response = session.request(
        #     method=method, url=self._build_url, params=kwargs, data=data
        # )

        # return response

    def _build_url(self):
        url = "/".join(self.session.base_url)
        return url

    def _validate_method(self, method):
        """Check the method on that endpoint is valid."""
        if self.methods is not None:
            if method not in self.methods:
                raise requests.exceptions.HTTPError(
                    "Method not available on this endpoint. Available methods: {}".format(
                        self.methods
                    )
                )
        return method

    def check_required(self, parameters: dict, method: str) -> dict:
        """Check that any request has the required parameters on the endpoint."""

        for parameter in self.required.get(method, []):
            if parameters is None:
                raise KeyError(
                    f"Query missing parameters. Required parameters: {self.required.get(method)}"
                )
            if parameters.get(parameter, None) is None:
                raise KeyError(
                    f"Query missing required parameter. Given: {parameters}. Required: {self.required.get(method)}"
                )

        return parameters


if __name__ == "__main__":
    session = ApiSession()
    session.new_endpoint()  # call endpoint
    session.existing_endpoint(method="PUT")  # should throw error
    session.call_existing_endpoint_wrapper()  # call the endpoint via the wrapper func
