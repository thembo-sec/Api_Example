import requests

BASE_URL = "SOME_URL"


class ApiSession(requests.Session):
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
        self.verify == ssl_verification
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
        wrapper method call
        """

        self.existing_endpoint = Endpoint(
            name="existing_endpoint", session=self, methods=["GET", "POST"]
        )

    def call_existing_endpoint_wrapper(self, endpoint_args):
        """Wrapper method for the `existing_endpoint` child"""
        return self.existing_endpoint(endpoint_args)


class Endpoint(object):
    def __init__(self, name, session: ApiSession, methods: list = None) -> None:
        self.name = name
        self.session = session
        self.methods = methods
        print(f"Creating endpoint at {session.base_url}/{self.name}")

    def __getattr__(self, name):
        return self.Endpoint(name)

    def __call__(self, *args, **kwargs) -> requests.Response:
        """Called when an unknown method is called on itself"""
        print(f"Calling {self.name}")

        method = self._validate_method(kwargs.pop("method", "GET"))
        data = kwargs.pop("data", None)

        # response = session.request(
        #     method=method, url=self._build_url, params=kwargs, data=data
        # )

        # return response

    def _build_url(self):
        url = "/".join(self.session.base_url)
        return url

    def _validate_method(self, method):
        if self.methods is not None:
            if method not in self.methods:
                raise requests.exceptions.HTTPError(
                    "Method not available on this endpoint. Available methods: {}".format(
                        self.methods
                    )
                )
        return method


if __name__ == "__main__":
    session = ApiSession()
    session.new_endpoint  # create the non-existing endpoint
    session.new_endpoint()  # call endpoint
    session.existing_endpoint(method="PUT")  # should throw error
    session.call_existing_endpoint_wrapper()  # call the endpoint via the wrapper func
