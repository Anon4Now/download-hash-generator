"""Module containing the Class for handling File changes"""

# Standard Library imports
from dataclasses import dataclass

# Third-party imports
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


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
        """Event Handler Configs"""
        _my_event_handler = PatternMatchingEventHandler(patterns=["*"])
        _my_event_handler.on_created = self.on_created_event  # overriding methods in PatternMatchingEventHandler class
        _my_event_handler.on_modified = self.on_modified_event  # overriding methods in PatternMatchingEventHandler class

        """Observer Configs/Start"""
        _my_observer = Observer()
        _my_observer.schedule(
            event_handler=_my_event_handler,
            path=self.path,
            recursive=True
        )
        _my_observer.start()

    @staticmethod
    def on_created_event(event) -> bool:
        print(event)
        return True

    @staticmethod
    def on_modified_event(event) -> None:
        pass
