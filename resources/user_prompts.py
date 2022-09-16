"""Module containing funcs that prompt the user for input and return bool"""

# Standard Library imports
import getpass
import platform

# Local App imports
from resources.utils import error_handler
from resources.errors import BadPromptResponseError


@error_handler
def start_watching_path() -> bool:
    """
    Function to prompt the user and determine if they want to start monitoring a path.
    :return: Boolean result of prompt (i.e. True = yes / False = no)
    :raise:
    """
    user_input = input("[?] Would you like to watch a path? [y/n] >> ").lower()
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False
    else:
        raise BadPromptResponseError


@error_handler
def start_watching_custom_path() -> str:
    """
    Function to prompt the user to determine if they want to watch
    a custom path.
    :return: String containing a custom path to watch
    """
    path = input("[?] Enter folder path to monitor, no quotes (i.e. C:/Users/username/Downloads) >> ")
    if path and isinstance(path, str):
        if '\\' in path:
            path = path.replace("\\", "/")
        return path
    else:
        raise BadPromptResponseError


@error_handler
def start_watching_default_path() -> str or None:
    """
    Function to prompt the user to determine if they want to use the OS
    default Download path
    :return: String containing either the default Download path, or None
    """
    os_name = platform.system()  # get OS details
    username = getpass.getuser()  # get current username
    default_path = input("[?] The default path to monitor is Downloads, do you want keep this? [y/n] >> ").lower()
    # determine if default path/custom path is being used
    if 'y' in default_path:
        if 'Windows' in os_name:
            path = f'C:/Users/{username}/Downloads'
            return path
        elif 'Linux' in os_name:
            path = f'/home/{username}/Downloads'
            return path
        elif 'Mac' in os_name:
            path = f'/Users/{username}/Downloads/'
            return path
    elif 'n' in default_path:
        return
    else:
        raise BadPromptResponseError


@error_handler
def check_vt_for_sha256_hash() -> bool:
    """
    Function to prompt user to determine if they would like to
    check Virus Total for information on the SHA256 hash. Will only be available
    to the user if they have set up a .env file in their dir.
    :return: Boolean result of the prompt (i.e. True = yes / False = no)
    """
    user_input = input("[?] Would you like to check the SHA256 hash against Virus Total? [y/n] >> ").lower()
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False
    else:
        raise BadPromptResponseError
