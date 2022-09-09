"""Module containing funcs that prompt the user for input and return bool"""

# Standard Library imports
import getpass
import platform


# TODO: NEED TO ADD CUSTOM EXCEPTION CLASS IN UTILS THAT HANDLES BAD PROMPT RESPONSES (BadPromptResponseError)
def start_watching_path() -> bool:
    """
    Function to prompt the user and determine if they want to start monitoring a path.
    :return: Boolean result of prompt (i.e. True = yes / False = no)
    :raise:
    """
    user_input = input("[?] Would you like to watch a path? [y/n] >> ")
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False


def start_watching_what_path() -> str:
    """
    Function to prompt the user to determine if they want to use the OS
    default Download path, or if they want to provide a custom path
    :return: String containing either the default Download path, or a custom path
    """
    osName = platform.system()  # get OS details
    username = getpass.getuser()  # get current username
    default_path = input("[?] The default path to monitor is Downloads, do you want keep this? [y/n] >> ")
    # determine if default path/custom path is being used
    # TODO: ADD MAC OS DEFAULT PATH
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
    """
    Function to prompt user to determine if they would like to
    check Virus Total for information on the SHA256 hash. Will only be available
    to the user if they have set up a .env file in their dir.
    :return: Boolean result of the prompt (i.e. True = yes / False = no)
    """
    user_input = input("[?] Would you like to check the SHA256 hash against Virus Total? [y/n] >> ")
    if 'y' in user_input:
        return True
    elif 'n' in user_input:
        return False
