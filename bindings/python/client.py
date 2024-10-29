from typing import List
import requests

from .endpoints import Endpoints
from .exceptions import EndpointResponseException
from .user import User
from .group import Group

class Client:
    def __init__(self, token: str, /):
        self.token = token
        self.user = None
        self.update_user()

    def update_user(self) -> None:
        response = self.request("GET", Endpoints.U_FETCH_SELF)
        json = response.json()

        self.user = User.from_dict(json)

    def fetch_joined_groups(self) -> List[Group]:
        response = self.request("GET", Endpoints.G_FETCH_JOINED)
        json = response.json()

        return [Group.from_dict(g) for g in json]

    def request(self, method: str | bytes, endpoint: str | bytes, request_args: dict = {}, /, *, excludeAuthToken: bool = False) -> requests.Response:
        if not excludeAuthToken:
            headers = request_args.get("headers")

            if headers is None:
                request_args["headers"] = {}
                headers = request_args["headers"]

            headers["Authorization"] = self.token

        response: requests.Response = requests.request(method, endpoint, **request_args)

        if response.status_code < 200 or response.status_code > 299:
            raise EndpointResponseException(f"Request failed with code {response.status_code}. Response content: {response.text}")

        return response