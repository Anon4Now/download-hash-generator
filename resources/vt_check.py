"""Module containing class and methods to parse the Virus Total API call"""

# Standard Library imports
import json
import datetime
from dataclasses import dataclass, field

# Third-party imports
import requests

# Local App imports
from resources.utils import error_handler


@dataclass
class VirusTotal:
    """Data-oriented class that holds the data around the
    Virus Total API calls.
    :param hash_sha256: (required) The string representation of the SHA256 hash
    :param api_endpoint: (required) The string representation Virus Total API endpoint to be called (env var)
    :param api_key: (required) The string representation Virus Total API key (env var)
    :param api_key_val: (required) The string representation of the Virus Total API key value (env var)
    """
    hash_sha256: str
    api_endpoint: str
    api_key: str
    api_key_val: str
    out_dict: dict = field(default_factory=dict, init=False, repr=False)

    @error_handler
    def __post_init__(self) -> None:
        """
        This post init check the API response to make sure there was no error.
        1. If no error found in response:
            1a. It will parse the response from the API for the "Last Analysis Time" and the "Last Analysis Stats"
            1b. It will update the instance dictionary with the data from the response
        2. If there is an error in response:
            2a. It will parse the response from the API for the "Error Code"
            2b. It will update the instance dictionary with the data from the response
        :return: None
        """
        try:
            if not self.response.get('error'):
                _analysis_date = datetime.datetime.fromtimestamp(
                    self.response.get('data').get('attributes').get('last_analysis_date'))
                self.out_dict['LastAnalysisDate'] = _analysis_date
                _analysis_stats = self.response.get('data').get('attributes').get('last_analysis_stats')
                self.out_dict['LastAnalysisStats'] = _analysis_stats
            else:
                _error_code = self.response.get('error').get('code')
                self.out_dict['error_code'] = _error_code
        except KeyError:
            raise

    @error_handler
    @property
    def response(self) -> dict:
        """
        This property method will make the API call and the loads response string
        :return: Dictionary containing the API response
        """
        # See if file has already been uploaded
        url = f"{self.api_endpoint}{self.hash_sha256}"

        headers = {
            "Accept": "application/json",
            self.api_key: self.api_key_val}
        response = requests.request("GET", url, headers=headers).text
        if response:
            return json.loads(response)
        else:
            raise Exception
