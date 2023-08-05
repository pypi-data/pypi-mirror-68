from typing import List


class Chain:
    def __init__(self, client: 'aiopipedrive.client.AbstractClient'):
        self.client = client
        self.path: List[str] = []

    def __getattr__(self, name: str) -> 'aiopipedrive.chain.Chain':
        self.path.append(name)

        return self

    def __call__(self, object_id=None) -> 'aiopipedrive.chain.Chain':
        if object_id is not None:
            self.path.append(str(object_id))

        return self

    def get(self, **query):
        return self.client.request('/'.join(self.path), 'GET', query=query)

    def add(self, **payload):
        return self.client.request('/'.join(self.path), 'POST', payload=payload)

    def update(self, **payload):
        return self.client.request('/'.join(self.path), 'PUT', payload=payload)

    def delete(self, **payload):
        return self.client.request('/'.join(self.path), 'DELETE', payload=payload)
