import aiohttp

from .abstract import AbstractClient
from .errors import PipedriveError


class Client(AbstractClient):

    "aiohttp-based client"

    def __init__(
        self,
        domain: str,
        token: str,
        version: str = 'v1',
        session: aiohttp.ClientSession = None,
    ):
        super().__init__(domain, token, version)

        self.session = session or aiohttp.ClientSession()

    async def request(
        self, path: str, method: str, query: dict = None, payload: dict = None
    ) -> dict:
        response = await self.session.request(
            method=method,
            url=self.get_endpoint_url(path),
            params={'api_token': self.token, **(query or {})},
            json=payload,
            headers={'Content-Type': 'application/json'},
        )

        try:
            data = await response.json()
        except ValueError:
            data = {}

        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as error:
            raise PipedriveError(
                message=data.get('error', 'Unknown error'), code=error.status,
            )

        return data
