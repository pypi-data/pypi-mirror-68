from requests import Session

from mondobrain.exceptions import InvalidCredentialsError

from .auth import APITokenAuth, JWTTokenAuth
from .credentials import CredentialsBase, JWTRefreshCredentials
from .util import join_url


class BaseUrlSession(Session):
    """
    An extension of `requests.Session` that smartly builds urls based on a `base_url`
    """

    def __init__(self, base_url="", **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        url = join_url(self.base_url, url)

        return super().request(method, url, **kwargs)


class APITokenSession(BaseUrlSession):
    """
    An extension of `BaseUrlSession` that specifies the authentication of the session
    using an API Key.

    If `auth` is overridden then the token auth will no longer be used
    """

    def __init__(self, token, **kwargs):
        super().__init__(**kwargs)
        self.auth = APITokenAuth(token)


class JWTSession(BaseUrlSession):
    """
    An extension of `BaseUrlSession` that specifies that smartly handles retreiving JWT
    Tokens based on passed Credentials.

    If `auth` is overridden then the token auth will no longer be used.
    """

    def __init__(self, credentials, base_url, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url

        self.auth, self.refresh_token = self.get_auth(credentials)

        self.hooks["response"] = [self.handle_401]

    def get_auth(self, credentials):
        if not isinstance(credentials, CredentialsBase):
            raise InvalidCredentialsError(
                f"credentials of type {type(credentials)} is not valid"
            )

        url = "auth/token"

        response = self.post(url, auth=credentials)

        if response.status_code == 401:
            error_detail = response.json()["detail"]
            raise InvalidCredentialsError(error_detail)

        tokens = response.json()

        auth = JWTTokenAuth(tokens["access"])
        refresh_token = JWTRefreshCredentials(tokens["refresh"])

        return auth, refresh_token

    def refresh_auth(self):
        url = "auth/token/refresh"
        response = self.post(url, auth=self.refresh_token)

        # todo: handle expired refresh token (24 hours)

        tokens = response.json()

        auth = JWTTokenAuth(tokens["access"])
        return auth

    def handle_401(self, res, **kwargs):
        """
            Takes the given response and tries to refresh token, if needed.

            Returns
            -------
            response: `requests.Response`
        """
        # If the status code isn't 401 then don't bother
        if res.status_code != 401:
            return res

        # If someone changed the auth of this session, then let this pass
        if "Bearer" not in res.request.headers["Authorization"]:
            return res

        prep = res.request.copy()

        # refresh token
        self.auth = self.refresh_auth()

        prep.prepare_auth(self.auth)

        _res = res.connection.send(prep, **kwargs)
        _res.history.append(res)
        _res.request = prep

        return _res
