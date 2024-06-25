from typing import Dict
import requests
import json

from variables import SQ_serverURL, SQ_token

class getCall:
    def __init__(self, API_NAME: str, PARAMS: Dict[str, str], JSON_NAME: str):
        self.url = SQ_serverURL + API_NAME
        self.bearer = "Bearer " + SQ_token
        self.header = {"Authorization": self.bearer}
        self.params = PARAMS
        self.jsonName = JSON_NAME
    
    def createJson(self):
        try:
            response = requests.get(self.url, headers=self.header, params=self.params)
            response.raise_for_status()
            try:
                data = response.json()
                with open(self.jsonName+".json", 'w') as f:
                    json.dump(data, f, indent=4)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                print("Response text:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
            
    def getJsonName(self):
        return self.jsonName+".json"
    
class postCall:
    def __init__(self, API_NAME: str, PARAMS: Dict[str, str]):
        self.url = SQ_serverURL + API_NAME
        self.bearer = "Bearer " + SQ_token
        self.header = {"Authorization": self.bearer}
        self.params = PARAMS
        
    def apply(self):
        try:
            response = requests.post(self.url, headers=self.header, params=self.params)
            response.raise_for_status()
            print("Status successfully changed.")
        except requests.exceptions.RequestException as e:
            print("Failed to change status:", e)