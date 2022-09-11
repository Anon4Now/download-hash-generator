import pytest

from resources import user_prompts
from resources.utils import BadPromptResponseError


def test_start_watching_path(monkeypatch):
    # Test that the user enters 'y' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert user_prompts.start_watching_path() is True

    # Test that the user enters 'n' when prompted
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert user_prompts.start_watching_path() is False

    # # Test error is raised if bad entry
    # (THIS REQUIRES THE error_handler DECORATOR TO BE REMOVED FROM FUNCTION)
    # monkeypatch.setattr('builtins.input', lambda _: "1")
    # with pytest.raises(BadPromptResponseError):
    #     user_prompts.start_watching_path()


def test_start_watching_what_path():
    pass


def test_check_vt_for_sha256_hash():
    pass
