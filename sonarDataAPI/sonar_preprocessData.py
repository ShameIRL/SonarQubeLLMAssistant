import json
import re
import os
from sonarDataAPI.sonar_requestsSpecific import getHotspotsList, getHotspotInfo, getHotspotSnippet, getRuleInfo, getVulnerabilitiesList, getIssueSnippet

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
            
    def addCodeHS(self):
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
        
    def addVulnerabilities(self):
        vulnerabilityList = getVulnerabilitiesList(project=self.projectName)
        vulnerabilityList.createJson()
        self.tempJson = vulnerabilityList.getJsonName()
        try:
            with open(self.tempJson, 'r') as f:
                jsonData = f.read()
                data = json.loads(jsonData)
                keys = [{"vulnerabilityKey": vulnerability["key"],
                        "status": vulnerability["status"],
                        "componentKey": vulnerability["component"],
                        "componentName": vulnerability["component"].split('/')[-1],
                        "componentPath": vulnerability["component"].split(':', 1)[1],
                        "lineStart": vulnerability["textRange"]["startLine"],
                        "lineEnd": vulnerability["textRange"]["endLine"],
                        "snippetStart": (int(vulnerability["textRange"]["startLine"])-10) if (int(vulnerability["textRange"]["startLine"])-10) > 0 else 1,
                        "snippetEnd": (int(vulnerability["textRange"]["startLine"])+10),
                        "ruleKey": vulnerability["rule"]
                        }for vulnerability in data["issues"]]
                with open(self.jsonName+".json", 'w') as f:
                    json.dump({"issues": keys}, f, indent=4)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        self.clearJson()
        
    def addRuleInfos(self):
        with open(self.jsonName+".json", 'r') as vulnerabilitiesJson:
            vulnerabilitiesData = json.load(vulnerabilitiesJson)     
        for vulnerability in vulnerabilitiesData["issues"]:
            ruleInfo = getRuleInfo(vulnerability["ruleKey"])
            ruleInfo.createJson()
            self.tempJson = ruleInfo.getJsonName()
            try:
                with open(self.tempJson, 'r') as f:
                    jsonData = f.read()
                    data = json.loads(jsonData)
                    vulnerability["ruleName"] = data["rule"]["name"]
                    for section in data["rule"]["descriptionSections"]:
                        if section["key"] == "introduction":
                            vulnerability["ruleDescription"] = re.sub(r'<[^>]+>', '', section["content"])
                        elif section["key"] == "how_to_fix":
                            vulnerability["ruleSolution"] = re.sub(r'<[^>]+>', '', section["content"])
                        elif section["key"] == "root_cause":
                            vulnerability["ruleCause"] = re.sub(r'<[^>]+>', '', section["content"])
                        elif section["key"] == "resources":
                            vulnerability["ruleResources"] = re.sub(r'<[^>]+>', '', section["content"])
            except json.JSONDecodeError as e:
                print("Error processing hotspot informations:", e)
        with open(self.jsonName+".json", 'w') as f:
            json.dump(vulnerabilitiesData, f, indent=4)
        self.clearJson()
        
    def addCodeV(self):
        with open(self.jsonName+".json", 'r') as vulnerabilitiesJson:
            vulnerabilitiesData = json.load(vulnerabilitiesJson)
        for vulnerability in vulnerabilitiesData["issues"]:
            snippet = getIssueSnippet(vulnerability["vulnerabilityKey"])
            snippet.createJson()
            self.tempJson = snippet.getJsonName()
            try:
                with open(self.tempJson, 'r') as f:
                    jsonData = f.read()
                    data = json.loads(jsonData)
                    eliminate_classes = ['k', 's', 'sym', 'c', 'cd']
                    pattern = r'<(?!\/?span\s+class="(?:(?!{}\\b).)*"\s*>)[^>]+>'.format('|'.join(eliminate_classes))
                    vulnerability["snippet"] = [{"code": "line " + str(line["line"]) + " = " + re.sub(pattern, '', line["code"])} for line in data[vulnerability["componentKey"]]["sources"]]
            except json.JSONDecodeError as e:
                print("Error processing hotspot informations:", e)
        with open(self.jsonName+".json", 'w') as f:
            json.dump(vulnerabilitiesData, f, indent=4)
        self.clearJson()
            
    def clearJson(self):
        try:
            os.remove(self.tempJson)
            print(f"File '{self.tempJson}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{self.tempJson}' not found.")
        except Exception as e:
            print(f"Error occurred while deleting file '{self.tempJson}': {e}")
                     
    def preprocessHS(self):
        self.addKeys()
        self.addInfos()
        self.addCodeHS()
        print(f"File '{self.jsonName}'.json created successfully.")
        
    def preprocessV(self):
        self.addVulnerabilities()
        self.addRuleInfos()
        self.addCodeV()
        print(f"File '{self.jsonName}'.json created successfully.")

    def getJsonName(self):
        return self.jsonName+".json"