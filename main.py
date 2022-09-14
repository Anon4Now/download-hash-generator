"""Main script that will open a cli interface with user"""

# Standard Library imports
import os
from pathlib import Path

# Third-party imports
from watchdog.observers import Observer

# Local App imports
from resources.user_prompts import (
    start_watching_path,
    start_watching_default_path,
    start_watching_custom_path
)
from resources.utils import (
    create_logger,
    error_handler,
    temp_file,
    my_event_handler,
    start_observer,
    stop_observer,
    get_envs
)
from resources.hash_generator import Hash
from resources.vt_check import use_virus_total

# Global vars
logger = create_logger()
does_temp_file_exist = Path(temp_file)


@error_handler
def main(path_to_watch: str) -> bool:
    """
    Main func that will start the loops to prompt user and print stdout.
    Will end the loops if the user either selects 'n' for appropriate responses,
    or if the user presses CTRL+C.
    :param path_to_watch: This is either the default os path for 'Downloads' or a custom path from user
    :return: None
    """
    #####################################
    # Observer Config & Start
    #####################################
    observer = Observer()
    observer.schedule(event_handler=my_event_handler, path=path_to_watch, recursive=True)
    start_observer(observer)

    logger.info("[!] Starting the watcher, to interrupt press 'CTRL+C'")
    # outermost loop keeping cli open
    while True:
        # inner loop that will monitor for events at the path set
        while observer.is_alive():  # TODO: TEST THE SNYK RECOMMENDATION FOR USING IF
            if does_temp_file_exist.is_file() and not os.stat(
                    temp_file).st_size == 0:  # does the temp file exist and does it have contents
                logger.info("[+] File downloaded, stopping observer and progressing")
                stop_observer(observer)  # kill the observer thread
                break  # end the inner loop
        logger.info("[!] Generating hashes for the downloaded file")
        hashes = Hash(text_file=temp_file)  # initialize the instance with the temp file name
        # Stdout to user what the file hashes are
        print(f' >> SHA256 -- {hashes.hash_sha256}')
        print(f' >> SHA1 -- {hashes.hash_sha1}')
        print(f' >> MD5 -- {hashes.hash_md5}')

        if get_envs():  # hide prompts unless env file exists in current directory
            return True if use_virus_total(hashes.hash_sha256) else False  # call the func in the vt_check module and check bool result

        break  # end the outermost loop


if __name__ == '__main__':
    try:
        if start_watching_path():  # prompt the user to see if they want to monitor a path
            path = start_watching_default_path()
            # ternary expression to determine which path will be used
            main(path_to_watch=path) if path else main(path_to_watch=start_watching_custom_path())
    finally:
        if os.path.exists(temp_file):  # if the temp file was created, delete it for next cycle
            os.remove(temp_file)
