"""Module containing Utility Functions"""

# Standard Library imports
import logging
import optparse

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

#####################################
# Get Environment Variables
#####################################
# LOGGING_LEVEL ----


#####################################
# Watchdog File Management Funcs
#####################################
def on_modified_event(event) -> None:
    get_event = str(event.src_path)  # get the src_path from event dict
    if 'exe' in get_event:
        with open("exe.txt", "w+") as file:  # write to the file for every modified event that is recieved
            file.write(get_event)


my_event_handler: PatternMatchingEventHandler = PatternMatchingEventHandler(patterns=["*"])
my_event_handler.on_modified = on_modified_event  # overriding methods in PatternMatchingEventHandler class


def start_observer(my_observer: Observer) -> None:
    my_observer.start()


def stop_observer(my_observer: Observer) -> None:
    my_observer.stop()


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


#######################################
# Option Parser
#######################################
parser = optparse.OptionParser()


def getArgs():
    parser.add_option(
        "-o",
        "--option",
        dest="sanitize_option",
        help="Requires either (delete OR modify)"
             "** delete option **\n"
             "- Deletes Internet Gateway"
             "- Deletes Subnets"
             "- Deletes Route Tables (not default)"
             "- Deletes NACL (not default)"
             "- Deletes SG (not default)"
             "- Deletes default VPC"
             "- Updates SSM parameter preferences to block public access\n\n"
             "** modify option **\n"
             "- Updates default NACL (removes inbound/outbound rules)"
             "- Updates default SG (removes inbound/outbound rules)"
             "- Updates SSM parameter preferences to block public access"
    )
    parsingInput = parser.parse_args()

    (options, args) = parsingInput

    if not options.sanitize_option:
        parser.error("[-] Please specify an option flag, --help for more info")
    else:
        return options
