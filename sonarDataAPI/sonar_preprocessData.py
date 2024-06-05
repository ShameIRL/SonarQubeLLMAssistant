import json
import re
import os
from sonarDataAPI.sonar_requestsSpecific import getHotspotsList, getHotspotInfo, getHotspotSnippet, getRuleInfo

class preprocessor:
    def __init__(self, PROJECT_NAME: str, JSON_NAME: str="PreprocessedData"):
        self.projectName = PROJECT_NAME
        self.jsonName = JSON_NAME
        self.tempJson: str = None
        
    def addKeys(self):
        hotspotsList = getHotspotsList(project=self.projectName)
        hotspotsList.createJson()
        self.tempJson = hotspotsList.getJsonName()
        try:
            with open(self.tempJson, 'r') as f:
                jsonData = f.read()
                data = json.loads(jsonData)
                keys = [{"hotspotKey": hotspot["key"]} for hotspot in data["hotspots"]]
                with open(self.jsonName+".json", 'w') as f:
                    json.dump({"hotspots": keys}, f, indent=4)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        self.clearJson()
            
    def addInfos(self):
        with open(self.jsonName+".json", 'r') as hotspotsJson:
            hotspotsData = json.load(hotspotsJson)
        for hotspot in hotspotsData["hotspots"]:
            hotspotInfo = getHotspotInfo(hotspot["hotspotKey"])
            hotspotInfo.createJson()
            self.tempJson = hotspotInfo.getJsonName()
            try:
                with open(self.tempJson, 'r') as f:
                    jsonData = f.read()
                    data = json.loads(jsonData)
                    hotspot["status"] = data["status"]
                    hotspot["ruleKey"] = data["rule"]["key"]
                    hotspot["ruleName"] = data["rule"]["name"]
                    hotspot["ruleRiskDescription"] = re.sub(r'<[^>]+>', '', data["rule"]["riskDescription"])
                    hotspot["ruleRiskAssessment"] = re.sub(r'<[^>]+>', '', data["rule"]["vulnerabilityDescription"])
                    hotspot["ruleRiskSolution"] = re.sub(r'<[^>]+>', '', data["rule"]["fixRecommendations"])
                    hotspot["componentKey"] = data["component"]["key"]
                    hotspot["componentName"] = data["component"]["name"]
                    hotspot["componentPath"] = data["component"]["path"]
                    hotspot["lineStart"] = data["textRange"]["startLine"]
                    hotspot["lineEnd"] = data["textRange"]["endLine"]
                    hotspot["snippetStart"] = (int(data["textRange"]["startLine"])-10) if (int(data["textRange"]["startLine"])-10) > 0 else 1
                    hotspot["snippetEnd"] = (int(data["textRange"]["endLine"])+10)
            except json.JSONDecodeError as e:
                print("Error processing hotspot informations:", e)
        with open(self.jsonName+".json", 'w') as f:
            json.dump(hotspotsData, f, indent=4)
        self.clearJson()
            
    def addCode(self):
        with open(self.jsonName+".json", 'r') as hotspotsJson:
            hotspotsData = json.load(hotspotsJson)
        for hotspot in hotspotsData["hotspots"]:
            snippet = getHotspotSnippet(hotspot["componentKey"], hotspot["snippetStart"], hotspot["snippetEnd"])
            snippet.createJson()
            self.tempJson = snippet.getJsonName()
            try:
                with open(self.tempJson, 'r') as f:
                    jsonData = f.read()
                    data = json.loads(jsonData)
                    eliminate_classes = ['k', 's', 'sym', 'c', 'cd']
                    pattern = r'<(?!\/?span\s+class="(?:(?!{}\\b).)*"\s*>)[^>]+>'.format('|'.join(eliminate_classes))
                    # introdurre -- re.sub(pattern, '', ) -- nella linea sotto qui: -- = " + re.sub(pattern, '', line["code"]) -- || o rimuoverlo e commentare linee sopra (= " + line["code"])
                    hotspot["snippet"] = [{"code": "line " + str(line["line"]) + " = " + re.sub(pattern, '', line["code"])} for line in data["sources"]]
            except json.JSONDecodeError as e:
                print("Error processing hotspot informations:", e)
        with open(self.jsonName+".json", 'w') as f:
            json.dump(hotspotsData, f, indent=4)
        self.clearJson()
            
    def clearJson(self):
        try:
            os.remove(self.tempJson)
            print(f"File '{self.tempJson}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{self.tempJson}' not found.")
        except Exception as e:
            print(f"Error occurred while deleting file '{self.tempJson}': {e}")
                     
    def preprocess(self):
        self.addKeys()
        self.addInfos()
        self.addCode()
        print(f"File '{self.jsonName}'.json created successfully.")

    def getJsonName(self):
        return self.jsonName+".json"