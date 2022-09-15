from main import main, call_vt_and_get_results
import pytest


@pytest.mark.skip(reason="the While loop will break this test, skipping")
def test_main_func() -> None:
    ...


def test_call_vt_and_get_results_200_response(mocker):
    """Testing the func to make sure a 200 response would be returned"""
    mocker.patch('main.retrieve_virus_total_results', return_value=({}, 200))
    expected = ({}, 200)
    actual = call_vt_and_get_results('71c8beb31074c53a59927f1874f0cce19bed8fd3be9edd93164511eb717c581c')
    assert expected[1] == actual[1]


def test_call_vt_and_get_results_404_response(mocker):
    """Testing the func to make sure a 404 response would be returned"""
    mocker.patch('main.retrieve_virus_total_results', return_value=({}, 404))
    expected = ({}, 404)
    actual = call_vt_and_get_results('11111111111111111111111111111111111111111111111111')
    assert expected[1] == actual[1]
