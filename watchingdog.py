from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


# Class to set Watchdog configs, and start the monitoring
class Watchdog:
    eventCheck = False  # used to determine if event was seen from on_created method

    # Set the config for the Watchdog process
    def __init__(self, path, patterns=["*"], ignore_patterns=None, ignore_directories=False, case_sensitive=True,
                 go_recursively=True):
        self.path = path
        self.patterns = patterns
        self.ignorePatterns = ignore_patterns
        self.ignoreDirectories = ignore_directories
        self.caseSensitive = case_sensitive
        self.goRecursive = go_recursively

    # Set the config for event handler process
    def eventHandlerConfig(self):
        # Event Handler Configurations
        my_event_handler = PatternMatchingEventHandler(self.patterns, self.ignorePatterns, self.ignoreDirectories,
                                                       self.caseSensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_modified = self.on_modified
        return my_event_handler

    # Watch for "create" events in file path
    @staticmethod
    def on_created(event):
        if event:
            Watchdog.eventCheck = True  # update class var for reference in main.py

    # Watch for "modified" events in file path and write event to txt file in py path
    @staticmethod
    def on_modified(event):
        getEvent = str(event.src_path)  # get the src_path from event dict
        fileName = "list.txt"  # create a file with this name
        with open(fileName, "w+") as file:  # write to the file for every modified event that is recieved
            file.write(getEvent)

    # Start the Observer, which is watch the path
    def startObserver(self):
        try:
            my_observer = Observer()  # instantiate the class object
            my_observer.start()  # start the observer
            my_observer.schedule(self.eventHandlerConfig(), self.path, recursive=self.goRecursive)  # provide config vals
            return True
        except FileNotFoundError:  # if manually entered path from user is not found, return None
            return
