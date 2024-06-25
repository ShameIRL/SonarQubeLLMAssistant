import json

class data: 
    def __init__(self, HOTSPOT_KEY: str, JSON_NAME: str="PreprocessedData"):
        self.jsonName = JSON_NAME
        self.data = self.readJson()
        self.hotspotKey = HOTSPOT_KEY
        
    def readJson(self):
        try:
            with open(self.jsonName+".json", 'r') as f:
                jsonData = f.read()
                return json.loads(jsonData)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
                    
    def getHS(self):
        if self.data == None:
            self.readJson()
        hotspots = self.data.get("hotspots", [])
        match = next((h for h in hotspots if h["hotspotKey"] == self.hotspotKey), None)
        if match:
            snippet_lines = []
            for line in match["snippet"]:
                code = line["code"]
                snippet_lines.append(f"{code}")
            return 1, match["ruleName"], match["ruleRiskDescription"], match["ruleRiskAssessment"], match["ruleRiskSolution"], match["componentPath"], match["lineStart"], match["snippetStart"], match["snippetEnd"], "\n".join(snippet_lines)
        else:
            return 0, "noRuleName", "noRuleRiskDescription", "noRuleRiskAssessment", "noRuleRiskSolution", "noCmponentPath", "noLineStart", "noSnippetStart", "noSnippetEnd", "noSnippet"
        
    def getV(self):
        if self.data == None:
            self.readJson()
        vulnerabilities = self.data.get("issues", [])
        match = next((v for v in vulnerabilities if v["vulnerabilityKey"] == self.hotspotKey), None)
        if match:
            snippet_lines = []
            for line in match["snippet"]:
                code = line["code"]
                snippet_lines.append(f"{code}")
            return 1, match["ruleName"], match["ruleDescription"], match["ruleSolution"], match["ruleCause"], match["ruleResources"], match["componentKey"], match["lineStart"], match["snippetStart"], match["snippetEnd"], "\n".join(snippet_lines)
        else:
            return 0, "noRuleName", "noRuleDescription", "noRuleSolution", "noRuleCause", "noRuleResources", "noComponentKey", "noLineStart", "noSnippetStart", "noSnippetEnd", "noSnippet"