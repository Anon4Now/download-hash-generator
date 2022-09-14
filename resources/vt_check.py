"""Module containing class and methods to parse the Virus Total API call"""

# Standard Library imports
import json
import datetime
import os
from dataclasses import dataclass, field
from typing import Any

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
        try:
            if not data.get('error'):
                return cls(
                    last_analysis_date=datetime.datetime.fromtimestamp(
                        data.get('data').get('attributes').get('last_analysis_date')),
                    last_analysis_stats=data.get('data').get('attributes').get('last_analysis_stats')
                )
            else:
                return cls(error_code=data.get('error').get('code'))
        except KeyError:
            raise


@error_handler
def retrieve_virus_total_results(sha256_hash: str, api_endpoint: str, api_key: str, api_key_val: str) -> dict:
    """
    This property method will make the API call and the loads response string
    :return: Dictionary containing the API response
    """
    # See if file has already been uploaded
    url = f"{api_endpoint}{sha256_hash}"

    headers = {
        "Accept": "application/json",
        api_key: api_key_val}
    response = requests.request("GET", url, headers=headers).text
    if response:
        return json.loads(response)
    else:
        raise Exception


def use_virus_total(sha256_hash: str) -> None:
    if check_vt_for_sha256_hash():  # prompt the user to see if a VT check is wanted
        logger.info("[!] Attempting to call Virus Total")
        vt_dict_results = retrieve_virus_total_results(
            sha256_hash=sha256_hash,
            api_endpoint=os.getenv('API_ENDPOINT'),
            api_key=os.getenv('API_key'),
            api_key_val=os.getenv('API_KEY_VAL'))  # pass the params to the API calling func
        vt = VirusTotal.from_dict(vt_dict_results)  # call the class method to parse the dict results

        if not vt.error_code:  # make sure there were no errors in API response
            # Stdout to user what the scan results are
            print(f">> Virus Total Results:")
            print(f" >>> Last Analysis Date:")
            print(f"      {vt.last_analysis_date}")
            print(f" >>> Last Analysis Stats:")
            for k, v in vt.last_analysis_stats.items():
                print(f"      {k} - {v}")
        else:  # if errors in API response, print them out
            print(f">> Virus Total Scan Failed with error code:\n {vt.error_code}")
