from sonarDataAPI.sonar_requestsBase import getCall, postCall

# GET APIs
class getHotspotsList(getCall):
    def __init__(self, project: str, inNewCodePeriod: str="false", onlyMine: str="false", p: str="1", ps: str="500", status: str="TO_REVIEW"):
        super().__init__("api/hotspots/search", {"inNewCodePeriod": inNewCodePeriod, "onlyMine": onlyMine, "p": p, "project": project, "ps": ps, "status": status}, "HotspotsList")

class getHotspotInfo(getCall):
    def __init__(self, hotspot: str):
        super().__init__("api/hotspots/show", {"hotspot": hotspot}, "HotspotInfo")
        
class getHotspotSnippet(getCall):
    def __init__(self, key: str, v_from: str, to: str):
        super().__init__("api/sources/lines", {"key": key, "from": v_from, "to": to}, "HotspotLines")

class getRuleInfo(getCall):
    def __init__(self, key: str):
        super().__init__("api/rules/show", {"key": key}, "RuleInfo")
        
class getVulnerabilitiesList(getCall):
    def __init__(self, project: str, s: str="FILE_LINE", issueStatuses: str="CONFIRMED,OPEN", types: str="VULNERABILITY", ps: str="100", facets: str="", additionalFields: str="", timeZone="Europe/Rome"):
        super().__init__("api/issues/search", {"components": project, "s": s, "issueStatuses": issueStatuses, "types": types, "ps": ps, "facets": facets, "additionalFields": additionalFields, "timeZone": timeZone}, "VulnerabilitiesList")

class getIssueSnippet(getCall):
    def __init__(self, issueKey: str):
        super().__init__("api/sources/issue_snippets", {"issueKey": issueKey}, "IssueSnippets")
        
# POST APIs
class postStatus(postCall):
    def __init__(self, key: str, resolution: str, comment: str, status: str = "REVIEWED"):
        super().__init__("api/hotspots/change_status", {"hotspot": key, "status": status, "resolution": resolution, "comment": comment})