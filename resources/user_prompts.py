"""Module containing funcs that prompt the user for input and return bool"""
import getpass
import platform


def start_watching_path() -> bool:
    user_input = input("[?] Would you like to watch a path? [y/n] >> ")
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False


def start_watching_what_path() -> str:
    osName = platform.system()  # get OS details
    username = getpass.getuser()  # get current username
    default_path = input("[?] The default path to monitor is Downloads, do you want keep this? [y/n] >> ")
    # determine if default path/custom path is being used
    if 'y' in default_path:
        if 'Windows' in osName:
            path = f'C:/Users/{username}/Downloads'
            return path
        elif 'Linux' in osName:
            path = f'/home/{username}/Downloads'
            return path
    elif 'n' in default_path:
        path = input("[?] Enter folder path to monitor, no quotes (i.e. C:/Users/username/Downloads) >> ")
        try:
            if '\\' in path:
                path = path.replace("\\", "/")
            return path
        except FileNotFoundError:
            raise


def check_vt_for_sha256_hash() -> bool:
    user_input = input("[?] Would you like to check the SHA256 hash against Virus Total? [y/n] >> ")
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False
