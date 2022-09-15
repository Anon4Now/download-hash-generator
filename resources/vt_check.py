"""Module containing class and functions to parse the Virus Total API call"""

# Standard Library imports
import json
import datetime
import os
from dataclasses import dataclass, field
from typing import Any, Tuple

# Third-party imports
import requests

from resources.user_prompts import check_vt_for_sha256_hash
# Local App imports
from resources.utils import error_handler, create_logger

logger = create_logger()


@dataclass
class VirusTotal:
    """Data-oriented class that holds the data around the
    Virus Total API calls.
    :param hash_sha256: (required) The string representation of the SHA256 hash
    :param api_endpoint: (required) The string representation Virus Total API endpoint to be called (env var)
    :param api_key: (required) The string representation Virus Total API key (env var)
    :param api_key_val: (required) The string representation of the Virus Total API key value (env var)
    """
    last_analysis_date: datetime = field(default_factory=Any)
    last_analysis_stats: dict = field(default_factory=dict)
    error_code: str = None

    @classmethod
    def from_dict(cls, data: dict) -> "VirusTotal Results":
        """
        This class method will take in a python structure (dict) and parse it for the class params
        :param data: A python dict obtained from Virus Total's APIs
        :return: String highlighting what data is being updated in class params
        """
        try:
            if not data.get('error'):
                return cls(
                    last_analysis_date=datetime.datetime.fromtimestamp(
                        data.get('data').get('attributes').get('last_analysis_date')),
                    last_analysis_stats=data.get('data').get('attributes').get('last_analysis_stats')
                )
            # TODO: THIS DOES NOT APPEAR TO BE WORKING WITH ERROR (ERROR: TypeError: error=Cannot instantiate typing.Any func=main)
            else:
                return cls(error_code=data.get('error').get('code'))
        except KeyError:
            raise


@error_handler
def retrieve_virus_total_results(sha256_hash: str, api_endpoint: str, api_key: str, api_key_val: str) -> Tuple[dict, int]:
    """
    This function will make the API call and the loads response string
    :param sha256_hash: (required) Hash derived from the Hash class needed for VT to check their DB
    :param api_endpoint: (required) The API endpoint stored as env variable
    :param api_key: (required) API key stored as env variable
    :param api_key_val: (required) API key value stored as env variable
    :return: Dictionary containing the API response
    """
    # See if file has already been uploaded
    url = f"{api_endpoint}{sha256_hash}"

    headers = {
        "Accept": "application/json",
        api_key: api_key_val}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), response.status_code
    elif response.status_code == 404:
        return {}, response.status_code
    else:
        raise Exception


def use_virus_total(sha256_hash: str) -> bool:
    """
    This function will dispatch the calls to the other elements in the module and
    will print out the Virus Total scan results to stdout.
    :param sha256_hash: (required) Hash derived from the Hash class needed for VT to check their DB
    :return: None
    """
    if check_vt_for_sha256_hash():  # prompt the user to see if a VT check is wanted
        logger.info("[!] Attempting to call Virus Total")
        vt_dict_results = retrieve_virus_total_results(
            sha256_hash=sha256_hash,
            api_endpoint=os.getenv('API_ENDPOINT'),
            api_key=os.getenv('API_key'),
            api_key_val=os.getenv('API_KEY_VAL'))  # pass the params to the API calling func
        vt = VirusTotal.from_dict(vt_dict_results[0])  # call the class method to parse the dict results

        if not vt.error_code:  # make sure there were no errors in API response
            # Stdout to user what the scan results are
            print(f">> Virus Total Results:")
            print(f" >>> Last Analysis Date:")
            print(f"      {vt.last_analysis_date}")
            print(f" >>> Last Analysis Stats:")
            for k, v in vt.last_analysis_stats.items():
                print(f"      {k} - {v}")
            return True
        else:  # if errors in API response, print them out
            print(f">> Virus Total Scan Failed with error code:\n {vt.error_code}")
            return False
