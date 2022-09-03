"""Module containing the Class for handling File changes"""

# Standard Library imports
from dataclasses import dataclass

# Third-party imports
from watchdog.observers import Observer



@dataclass
class File:
    path: str
    """Class that contains attrs and methods related
    to the tracking and event raising events around
    file changes in the monitored path
    :param path: String that contains either the OS default download path or a custom user path
    """

    def __post_init__(self) -> None:
        """
        Post initialized instance attrs needed for class methods
        :_my_event_handler: Setting the event handler config to check for all events (https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.observers.Observer)
        :return: None
        """

