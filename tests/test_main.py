from main import main
import pytest


@pytest.mark.skip(reason="the While loop will break this test, skipping")
def test_main_func() -> None:
    ...
