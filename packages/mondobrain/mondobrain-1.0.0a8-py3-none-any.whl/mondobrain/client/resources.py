from mondobrain.exceptions import AuthenticationClassNotAllowed

from .auth import APITokenAuth
from .util import join_url


class APIResource:
    allowed_authentication = None

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = join_url(base_url, "")

    def __call__(self, id=None):
        url = self.base_url

        if id is not None:
            url = join_url(url, str(id))

        return APIResource(self.session, url)

    def _check_allowed_authentication(self):
        auth_allowed = self.allowed_authentication
        auth_ses = self.session.auth
        if auth_allowed is not None:
            if not any(isinstance(auth_ses, ac) for ac in auth_allowed):
                aas = ", ".join(ac.__name__ for ac in auth_allowed)
                raise AuthenticationClassNotAllowed(
                    (
                        f"Authentication of type {auth_ses.__class__.__name__} is"
                        f" not allowed. Only the following types are allowed: {aas}"
                    )
                )

    def get(self):
        self._check_allowed_authentication()
        return self.session.get(self.base_url)

    @property
    def _constructor(self):
        return APIResource

    def __getattr__(self, item):
        url = join_url(self.base_url, item)
        return self._constructor(self.session, url)


class APITokenOnlyAPIResource(APIResource):
    allowed_authentication = [APITokenAuth]


class SolverAPIResource(APITokenOnlyAPIResource):
    @property
    def _constructor(self):
        return SolverAPIResource

    def post(self, data=None, **kwargs):
        self._check_allowed_authentication()
        return self.session.post(self.base_url, data=data, **kwargs)
