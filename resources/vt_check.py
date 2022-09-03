import requests, os, datetime
from dotenv import load_dotenv


# Run SHA256 against Virus Total DB
class VTChecking:
    load_dotenv()  # load .env file containing vars

    # Set env vars during object instantiation
    def __init__(self):
        self.API_ENDPOINT = os.getenv('API_ENDPOINT')
        self.API_KEY = os.getenv('API_KEY')
        self.API_KEY_VAL = os.getenv('API_KEY_VAL')

    # Use GET to check to see if data exists on hash
    def hashExists(self, checkHash):
        # See if file has already been uploaded
        url = f"{self.API_ENDPOINT}{checkHash}"

        headers = {
            "Accept": "application/json",
            self.API_KEY: self.API_KEY_VAL}
        response = requests.request("GET", url, headers=headers)
        return response.text

    # Parse the response from VT API
    @staticmethod
    def parseJson(content):
        lastStatsDict = {}  # empty dict to use as data store

        # extract useful data from JSON response
        extractLastAnalysisDate = datetime.datetime.fromtimestamp(
            content['data']['attributes']['last_analysis_date'])
        extractLastAnalysisStats = content['data']['attributes']['last_analysis_stats']
        print(f'Last Analysis Date : {extractLastAnalysisDate}')
        print(f'Last Analysis Stats:')
        for key in extractLastAnalysisStats:
            lastStatsDict[key] = extractLastAnalysisStats[key]
            print(F'   {key}: {extractLastAnalysisStats[key]}')

        # make determination based on content
        for key in lastStatsDict:
            if key == 'malicious':
                if lastStatsDict[key] == 0:
                    print(f'\nBased on results, the file appears safe')
                elif 0 < lastStatsDict[key] < 2:
                    print(f'\nSome vendors flagged this file, consider additional research')
                elif lastStatsDict[key] > 2:
                    print(f'\nThis file may be malicious, consider not downloading')

    # If error exists in JSON response, parse the error
    @staticmethod
    def checkError(content):
        extractErrorCode = content['error']['code']
        if extractErrorCode == 'NotFoundError':
            print(
                f'This file has not been uploaded to Virus Total before -- consider uploading the file for scanning at \n"https://www.virustotal.com/gui/home/upload"')

        elif extractErrorCode != 'NotFoundError':
            print(f'Error returned from VT is {extractErrorCode}')
