import requests
import json
import datetime
from dataclasses import dataclass, field


@dataclass
class VirusTotal:
    hash_sha256: str
    api_endpoint: str
    api_key: str
    api_key_val: str
    out_dict: dict = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        if not self.response.get('error'):
            _analysis_date = datetime.datetime.fromtimestamp(
                self.response.get('data').get('attributes').get('last_analysis_date'))
            self.out_dict['LastAnalysisDate'] = _analysis_date
            _analysis_stats = self.response.get('data').get('attributes').get('last_analysis_stats')
            self.out_dict['LastAnalysisStats'] = _analysis_stats
        else:
            _error_code = self.response.get('error').get('code')
            self.out_dict['error_code'] = _error_code

    @property
    def response(self) -> dict:
        # See if file has already been uploaded
        url = f"{self.api_endpoint}{self.hash_sha256}"

        headers = {
            "Accept": "application/json",
            self.api_key: self.api_key_val}
        response = requests.request("GET", url, headers=headers).text
        return json.loads(response)
