class CredentialsBase(object):
    """Base class that all credential implementations derive from
    It should be noted that these classes will operate on a
    :class:`requests.PreparedRequest` and not a :class:`requests.Request`
    """

    def __call__(self, r):
        raise NotImplementedError("Credential hooks must be callable.")


class BasicCredentials(CredentialsBase):
    """Username & Password holder"""

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def __call__(self, r):
        r.prepare_body({"username": self.__username, "password": self.__password}, None)
        return r


class JWTRefreshCredentials(CredentialsBase):
    """JWT Token credentialer"""

    def __init__(self, refresh):
        self.__refresh = refresh

    def __call__(self, r):
        r.prepare_body({"refresh": self.__refresh}, None)
        return r
