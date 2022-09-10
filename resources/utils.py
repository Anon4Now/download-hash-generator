"""Module containing Utility Functions"""

# Standard Library imports
import logging

# Third-party imports
from dotenv import load_dotenv, find_dotenv
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


temp_file = 'temp.txt'  # name of the temp file created and deleted by script


#####################################
# Get Environment Variables
#####################################
# LOGGING_LEVEL ----

# DOTENV ENVIRONMENT VARIABLES
def get_envs() -> bool:
    """
    A function that checks that a dotenv file exists in the dir,
    and if yes it will load the env vars.
    :return: Boolean result to depict whether the dotenv file exists (i.e. True = exists / False = doesn't exist)
    """
    if find_dotenv():
        load_dotenv()
        return True
    else:
        return False


#####################################
# Create logger func
#####################################
def create_logger() -> logging:
    """
    Create a logger
    :return: logger
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
    log = logging.getLogger()
    # log.setLevel(logging.INFO)

    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    return log


logger = create_logger()  # create logger func


###########################
# Custom Error Handler func
###########################

# def error_handler(func):
#     # exception handling decorator function
#
#     def inner_func(*args, **kwargs):
#         try:
#             result = func(*args, **kwargs)
#             return result
#         except botocore.exceptions.NoCredentialsError as err:
#             logger.error("NoCredentialsError: error=%s func=%s", err.fmt, func.__name__)
#         except botocore.exceptions.NoRegionError as err:
#             logger.error("NoRegionError: error=%s func=%s", err.fmt, func.__name__)
#         except botocore.exceptions.ClientError as err:
#             logger.error("ClientError: error=%s func=%s", err, func.__name__)
#         except Exception as err:
#             logger.error("GeneralException: error=%s func=%s", err, func.__name__)
#
#     return inner_func

#####################################
# Watchdog File Management Funcs
#####################################
def on_modified_event(event) -> None:
    """
    Function that overwrites a method of the same name in the PatternMatchingEventHandler class.
    Used to pass events from the watcher and perform actions on "modify" events.
    ** IMPORTANT ** -- Modifying this function will change the behavior of the whole program
    :param event: An event in the form of a class, used to write info to temp_file.txt
    :return: None
    """
    get_event = str(event.src_path)  # get the src_path from event dict
    if 'exe' in get_event:
        with open(temp_file, "w+") as file:  # write to the file for any matching modified event that is received
            file.write(get_event)


# Needed vars and assignments for watcher to function properly
my_event_handler: PatternMatchingEventHandler = PatternMatchingEventHandler(patterns=["*"])
my_event_handler.on_modified = on_modified_event  # overriding methods in PatternMatchingEventHandler class


def start_observer(my_observer: Observer) -> None:
    """
    Function to start the watcher, which calls a method on the Observer class
    :param my_observer: Instantiated instance of the Observer class from main.py
    :return: None
    """
    my_observer.start()


def stop_observer(my_observer: Observer) -> None:
    """
    Function to stop the watcher, which calls a method on the Observer class
    :param my_observer: Instantiated instance of the Observer class from main.py
    :return: None
    """
    my_observer.stop()
