from requests.auth import AuthBase


class JWTTokenAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self._token}"
        return r


class APITokenAuth(AuthBase):
    """API Key credentialer"""

    def __init__(self, token):
        self.__token = token

    def __call__(self, r):
        r.headers["X-API-Token"] = self.__token
        return r
