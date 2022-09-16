"""Module containing the test cases for the vt_check module"""

# Standard Library imports
import json

# Third-party imports
import pytest

# Local App imports
from resources import vt_check
from main import call_vt_and_get_results


@pytest.fixture
def get_results_from_vt():
    """Loads the 200 response saved JSON data from the path and returns it as pytest fixture"""
    with open('tests/json_files/results.json', 'rb') as f:
        return json.load(f)


@pytest.fixture
def get_error_results_from_vt():
    """Loads the 404 response saved JSON data from the path and returns it as pytest fixture"""
    with open('tests/json_files/no_results.json', 'rb') as f:
        return json.load(f)


def test_api_call_200_response(mocker, get_results_from_vt):
    """Testing the API call with the 200 response data"""
    mocker.patch('main.retrieve_virus_total_results', return_value=(get_results_from_vt, 200))  # documentation explaining this mocker (https://changhsinlee.com/pytest-mock/)
    expected = get_results_from_vt
    actual = call_vt_and_get_results('71c8beb31074c53a59927f1874f0cce19bed8fd3be9edd93164511eb717c581c')
    assert expected == actual[0]


def test_api_call_404_response(mocker, get_error_results_from_vt):
    """Testing the API call with the 404 response data"""
    mocker.patch('main.retrieve_virus_total_results', return_value=(get_error_results_from_vt, 404))
    expected = get_error_results_from_vt
    actual = call_vt_and_get_results('1111111111111111111111111111111111111111111')
    assert expected == actual[0]


def test_use_virus_total_results(get_results_from_vt, get_error_results_from_vt):
    """Testing that the use_virus_total func gets back the correct bool result based on status code from JSON response"""
    assert vt_check.use_virus_total(get_results_from_vt) is True
    assert vt_check.use_virus_total(get_error_results_from_vt) is False


def test_virus_total_class(get_results_from_vt, get_error_results_from_vt):
    """Testing the cls method to make sure the correct initializer variables are updated depending on the JSON response"""
    vt_results = vt_check.VirusTotal.from_dict(get_results_from_vt)
    assert vt_results.last_analysis_stats is not None
    assert vt_results.last_analysis_date is not None
    assert vt_results.error_code is None

    vt_error_results = vt_check.VirusTotal.from_dict(get_error_results_from_vt)
    assert vt_error_results.error_code is not None
    assert vt_error_results.last_analysis_date is None
    assert vt_error_results.last_analysis_stats is None
