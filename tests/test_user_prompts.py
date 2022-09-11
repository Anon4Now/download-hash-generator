"""Module containing tests for user_prompts functions"""

# Standard Library imports
import getpass

# Third-party imports
import pytest  # use this import when testing without error_handler

# Local App imports
from resources import user_prompts
from resources.utils import BadPromptResponseError  # use this import when testing without error_handler


def test_start_watching_path(monkeypatch) -> None:
    """Test the function to check whether the user passes [y/n] in prompt response"""

    # Test that the user enters 'y' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert user_prompts.start_watching_path() is True

    # Test that the user enters 'n' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert user_prompts.start_watching_path() is False

    # Test to see if error is raised if there is a bad entry
    # (THIS REQUIRES THE @error_handler DECORATOR TO BE REMOVED FROM FUNCTION TO TEST)
    # monkeypatch.setattr('builtins.input', lambda _: 1)
    # with pytest.raises(BadPromptResponseError):
    #     user_prompts.start_watching_path()


def test_start_watching_what_path(monkeypatch) -> None:
    """Test the function to check whether it returns either default path
    or that the user enters a custom path to monitor as a string
    """
    # Test that the user enters 'y' when prompted
    username = getpass.getuser()
    yes_paths = [f'C:/Users/{username}/Downloads', f'/home/{username}/Downloads', f'/Users/{username}/Downloads/']
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert user_prompts.start_watching_default_path() in yes_paths

    # Test that the user enters 'n' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert user_prompts.start_watching_default_path() is None

    # Test to see if error is raised if there is a bad entry
    # (THIS REQUIRES THE @error_handler DECORATOR TO BE REMOVED FROM FUNCTION TO TEST)
    # monkeypatch.setattr('builtins.input', lambda _: 1)
    # with pytest.raises(BadPromptResponseError):
    #     user_prompts.start_watching_default_path()


def test_start_watching_custom_path(monkeypatch) -> None:
    """Test the function to check whether it returns a custom
    path to monitor as a string
    """

    # Test that the return value matches the user input
    monkeypatch.setattr('builtins.input', lambda _: "path")
    assert user_prompts.start_watching_custom_path() == "path"

    # Test that if the user enters '\\' character, it is converted to '/'
    monkeypatch.setattr('builtins.input', lambda _: "C:\\Users")
    assert user_prompts.start_watching_custom_path() == "C:/Users"

    # Test to see if error is raised if there is a bad entry
    # (THIS REQUIRES THE @error_handler DECORATOR TO BE REMOVED FROM FUNCTION TO TEST)
    # monkeypatch.setattr('builtins.input', lambda _: 1)
    # with pytest.raises(BadPromptResponseError):
    #     user_prompts.start_watching_custom_path()


def test_check_vt_for_sha256_hash(monkeypatch) -> None:
    """Test the function to check whether the user passes [y/n] in prompt response"""

    # Test that the user enters 'y' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert user_prompts.check_vt_for_sha256_hash() is True

    # Test that the user enters 'y' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert user_prompts.check_vt_for_sha256_hash() is False

    # Test to see if error is raised if there is a bad entry
    # (THIS REQUIRES THE @error_handler DECORATOR TO BE REMOVED FROM FUNCTION TO TEST)
    # monkeypatch.setattr('builtins.input', lambda _: 1)
    # with pytest.raises(BadPromptResponseError):
    #     user_prompts.check_vt_for_sha256_hash()
