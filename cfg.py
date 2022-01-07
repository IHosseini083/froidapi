from configparser import ConfigParser
from typing import Dict, Iterable, List, Union


def config_loader(path: Union[str, Iterable[str]] = "config.ini") -> ConfigParser:
    """Loads the configuration file and returns a `ConfigParser` object.

    Parameters:
        path (`str` | `Iterable[str]`): Path or list of paths to the configuration file.

    Returns:
        `ConfigParser`: The configuration file as a `ConfigParser` object.
    """
    cfg = ConfigParser(comment_prefixes=("#", ";"))
    cfg.read(path)
    return cfg


cfg = config_loader()

####### Main App Config #######
APP_NAME: str = cfg["APP"]["NAME"]
"""Name of the application."""
APP_VERSION: str = cfg["APP"]["VERSION"]
"""Current version of the application."""
APP_DESCRIPTION: str = cfg["APP"]["DESCRIPTION"]
"""A short description of the application."""
CONTACT_INFO: Dict[str, str] = dict(cfg["CONTACT"])
"""Contact information of the developer."""

####### Common Config #######
DEBUG: bool = cfg["COMMON"].getboolean("DEBUG")
"""Set to `True` to see the error message in the browser."""

####### CORS Config #######
ORIGINS: List[str] = cfg["CORS"]["ORIGINS"].split(",")
"""List of origins that are allowed to access the API."""
ALLOW_CREDENTIALS: bool = cfg["CORS"].getboolean("ALLOW_CREDENTIALS")
"""Whether or not to allow credentials to be sent with the request."""
ALLOW_METHODS: List[str] = cfg["CORS"]["ALLOW_METHODS"].split(",")
"""List of HTTP methods that are allowed to access the API."""
ALLOW_HEADERS: List[str] = cfg["CORS"]["ALLOW_HEADERS"].split(",")
"""Which headers are allowed to be sent with the request."""

####### Docs Config #######
DOCS_URL: str = cfg["DOCS"]["URL"]
"""URL to the API documentation page."""
OPENAPI_URL: str = cfg["DOCS"]["OPENAPI_URL"]
"""URL of the OpenAPI specification `.json` file."""
DOCS_TITLE: str = cfg["DOCS"]["TITLE"]
"""Title of the API documentation page."""
DOCS_FAVICON_URL: str = cfg["DOCS"]["FAVICON"]
"""URL or path to the favicon of the API documentation page."""


if __name__ == "__main__":
    print(ALLOW_CREDENTIALS)
