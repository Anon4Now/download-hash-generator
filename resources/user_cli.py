import getpass, platform, sys, time
from watchingdog import Watchdog


# Class to get info/inputs from user
class GetUserOptions:

    # Check OS, check username, return path in correct format
    @staticmethod
    def startWatchingPath():
        osName = platform.system()  # get OS details
        username = getpass.getuser()  # get current username
        defaultPath = input("[+] The default path to monitor is Downloads, do you want keep this? [y/n] >> ")

        # determine if default path/custom path is being used
        if defaultPath == 'y':
            if 'Windows' in osName:
                path = f'C:/Users/{username}/Downloads'
                return path
            elif 'Linux' in osName:
                path = f'/home/{username}/Downloads'
                return path
        elif defaultPath == 'n':
            path = input("[+] Enter path to folder to monitor (remove quotations '\"')? >> ")
            if '\\' in path:
                path = path.replace("\\", "/")
            return path

    # Return countdown to CLI to download file
    @staticmethod
    def countDownToDownload():
        for i in range(300, -1, -1):  # set the time to download
            if not Watchdog.eventCheck:  # check to see if an event was seen by Watchdog
                if i == 0:  # if counter == 0 - clear stdout, end loop, and return None
                    sys.stdout.flush()
                    return

                else:  # if counter != 0 - stdout the current int using carriage return to replace previous int
                    sys.stdout.write("\r" + str(i))
                    sys.stdout.flush()
                    time.sleep(1)

            else:  # if Watchdog sees an event - print message, clear stdout, end loop return True
                print(f'\r[+] File seen - generating hashes...\n')
                sys.stdout.flush()
                return True

    # Prompt the user if they wish to run SHA256 by VT
    @staticmethod
    def useVirusTotal():

        vt = input("Would you like to check the SHA256 hash against VirusTotal DB? [y/n] >> ")

        if vt == 'y':
            return True
        elif vt == 'n':
            return False
        else:
            return

    # Exit program
    @staticmethod
    def stopWatching():
        sys.exit(-1)
