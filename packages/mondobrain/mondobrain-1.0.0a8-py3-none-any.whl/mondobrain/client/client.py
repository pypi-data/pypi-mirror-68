from .credentials import BasicCredentials
from .resources import APIResource, SolverAPIResource
from .sessions import APITokenSession, JWTSession


class Client:
    def __init__(
        self,
        apiKey=None,
        username=None,
        password=None,
        domain="staging.mondobrain.com",
        https=True,
    ):
        # endpoint configuration
        scheme = "https://" if https else "http://"
        base_url = scheme + domain + "/api/v0.2/"

        if username is not None and password is not None and apiKey is not None:
            raise ValueError(
                "`username` & `password` must be unset when `apiKey` is used"
            )

        session = None

        if apiKey is not None:
            session = APITokenSession(apiKey, base_url=base_url)

        if username is not None and password is not None:
            creds = BasicCredentials(username, password)
            session = JWTSession(creds, base_url=base_url)

        if session is None:
            raise TypeError(
                (
                    "Missing authorization arguments."
                    "Need `apiKey` or `username` & `password` arguments"
                )
            )

        self.session = session

        # setup resources
        # note: this is not end design yet
        self.portals = APIResource(self.session, "portals")

        # these ones are special... works still needed
        self._solver = SolverAPIResource(self.session, "sdk/process/solve")

    def request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)
