import requests

from .abstract import AbstractClient
from .errors import PipedriveError


class Client(AbstractClient):

    """requests-based client"""

    def request(
        self, path: str, method: str, query: dict = None, payload: dict = None
    ) -> dict:
        response = requests.request(
            method,
            self.get_endpoint_url(path),
            json=payload,
            params={'api_token': self.token, **(query or {})},
            headers={'Content-Type': 'application/json'},
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise PipedriveError(
                message=data.get('error', 'Unknown error'),
                code=error.response.status_code,
            )

        return data
