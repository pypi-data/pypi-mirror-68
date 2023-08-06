# from mondobrain.client.exceptions import *  # noqa: F401,F403


class InvalidCredentialsError(Exception):
    pass


class InvalidTargetError(ValueError):
    """
    Custom error that gets raised when a specified modality
    does not exist for a variable
    """


class AuthenticationClassNotAllowed(Exception):
    pass
