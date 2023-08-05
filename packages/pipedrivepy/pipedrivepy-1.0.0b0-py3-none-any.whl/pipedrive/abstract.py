from .chain import Chain


class AbstractClient:

    ENDPOINT = 'https://{domain}.pipedrive.com/api/{version}/{path}'

    def __init__(self, domain: str, token: str, version: str = 'v1'):
        self.domain = domain
        self.token = token
        self.version = version

    def __getattr__(self, name: str) -> Chain:
        return Chain(self).__getattr__(name)

    def get_endpoint_url(self, path: str) -> str:
        return self.ENDPOINT.format(domain=self.domain, version=self.version, path=path)
