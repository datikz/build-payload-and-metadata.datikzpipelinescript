"""Function implementation to obtain the configuration"""
from yaml import safe_load


def getYaml(route):
    """Returns the configuration as a dictionary

    Parameters
    ----------
    route: str
        Path of the configuration file which at start is './docs/info.yml'.

    Returns
    -------
    dict: Configuration inserted in the configuration file
    """
    with open(route, encoding="utf8") as file:
        return safe_load(file.read().replace("'", ""))
