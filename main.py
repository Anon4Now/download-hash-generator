import os
from hashlib import sha256
import sys
from pathlib import Path
from watchdog.observers import Observer

from resources.user_prompts import (
    start_watching_path,
    start_watching_what_path
)
from resources.hash_generator import Hash
from resources import (
    create_logger,
    my_event_handler,
    start_observer,
    stop_observer
)

logger = create_logger()


def main(path_to_watch: str) -> None:
    observer = Observer()
    observer.schedule(event_handler=my_event_handler, path=path_to_watch, recursive=True)
    text_file = Path('exe.txt')
    start_observer(observer)
    while True:
        while observer.is_alive():
            if text_file.is_file() and not os.stat('exe.txt').st_size == 0:
                logger.info("[+] File downloaded, stopping observer and progressing")
                stop_observer(observer)
                break
        logger.info("[!] Generating hashes for the downloaded file")
        hashes = Hash(text_file='exe.txt')
        # TODO: NEED TO PROMPT THE USER TO SEE IF THEY WANT TO CHECK VT (IF ENV FILE IS PRESENT)
        break


if __name__ == '__main__':
    if start_watching_path():
        user_path = start_watching_what_path()
        logger.info("[!] Starting the watcher, to interrupt press 'CTRL+C'")
        main(path_to_watch=user_path)

# import os, time, json
#
# from watchingdog import Watchdog
# from hash_generator import HashGenerator
# from user_cli import GetUserOptions
# from vt_check import VTChecking
#
# fileName = "list.txt"  # name of temp file
#
#
# # Will reset script upon init in case reset did not occur at end
# def clean_script():
#     if os.path.exists(fileName):
#         os.remove(fileName)
#
#
# if __name__ == '__main__':
#     clean_script()  # run clean script to remove old list file
#
#     # start outer user loop
#     while True:
#         userInput = input("\r[+] Would you like to start watching a folder? [y/n] >> ")
#         getArgs = GetUserOptions()  # instantiate GetUserOptions Class Object
#
#         # check initial response from user
#         if userInput == 'y':
#             path = getArgs.startWatchingPath()  # call Watchdog class for additional prompts around path to watch
#             watcher = Watchdog(path)  # instantiate Watchdog object with path
#             isStarted = watcher.startObserver()  # start the observer
#
#             # check to see if file path provided by user was not found
#             if isStarted:
#                 print("[+] Seconds left to download file")
#                 checkForFile = getArgs.countDownToDownload()  # start the download counter
#
#                 # check if file was attempted to be downloaded during timer
#                 if not checkForFile:
#                     print("\r[-] No file detected, returning to start...")
#                     time.sleep(3)
#                     continue  # return to start of outer loop
#                 else:
#                     hashGen = HashGenerator(fileName)  # instantiate HashGenerator object with update file
#
#                     # generate hashes
#                     time.sleep(
#                         10)  # provide enough time for watcher to get the final file type - can be problematic with large files
#                     sha256HASH = hashGen.startHash()  # call hash gen and return val
#                     time.sleep(5)
#                     clean_script()
#
#                 # see if user has set up API file in directory
#                 if os.path.exists(".env"):
#                     # start inner loop
#                     while True:
#                         useAPI = getArgs.useVirusTotal()  # prompt user if they want to use API check
#
#                         # if yes is given
#                         if useAPI:
#                             vt = VTChecking()  # instantiate object
#                             response = vt.hashExists(sha256HASH)  # send hash to VT API call
#                             checkIDJson = json.loads(response)  # parse JSON to str
#
#                             # if error is not present in response
#                             if 'error' not in checkIDJson:
#                                 vt.parseJson(checkIDJson)
#                                 break
#                             # if error is present in response
#                             if 'error' in checkIDJson:
#                                 vt.checkError(checkIDJson)
#                                 break
#
#                         # is no is given
#                         elif not useAPI:
#                             checkInput = input("[+] Would you like to exit to start? [y/n] >> ")
#                             if checkInput == 'y':
#                                 break  # stop inner loop
#                             elif checkInput == 'n':
#                                 continue  # loop back to start of inner loop
#                         else:
#                             print("[-] Unknown entry, please use 'y' or 'n'...")
#                             continue  # loop back to start of inner loop
#                     time.sleep(1)
#                     clean_script()
#
#             # if manual file path provided by user is not found
#             else:
#                 print("[-] File path unknown, returning to start...")
#
#         # if user does not want to monitor folder
#         elif userInput == 'n':
#             userInput = input("[+] Do you want to exit? [y/n] >> ")
#             if userInput == 'y':
#                 print("[+] Closing program...")
#                 getArgs.stopWatching()  # call method to exit program
#             elif userInput == 'n':
#                 continue  # loop back to starting prompt - outer loop
#             else:
#                 print("[-] Unknown input, please enter 'y' or 'n'...")
#                 continue  # loop back to starting prompt - outer loop
