import os
import json
from datetime import datetime
from json.decoder import JSONDecodeError

from sonarDataAPI.sonar_requestsSpecific import postHotspotStatus
from sonarDataAPI.sonar_preprocessData import preprocessor
from sonarDataAPI.sonar_getData import data
from openAPI.openAI_request import getCompletion
from openAPI.openAI_parse import answer_parse

from variables import project_Name
from prompts.promptsHS import PROMPT_JSON as PROMPT, PROMPT_VALIDATION
from prompts.promptQ import PROMPT_QHS as PROMPT_Q

projectName = project_Name
exePreprocessor = preprocessor(projectName, "PreprocessedHotspotsData")
exeJson = exePreprocessor.getJsonName()
if exeJson and not os.path.isfile(exeJson): 
    exePreprocessor.preprocessHS()
    
with open(exeJson, "r") as file:
    jsonData = json.load(file)
hotspots = jsonData.get("hotspots", [])
keys = [h["hotspotKey"] for h in hotspots]
print(f"Keys found:\n{keys}")

for currKey in keys:
    exeData = data(currKey, "PreprocessedHotspotsData")
    check, ruleName, ruleRiskDescription, ruleRiskAssessment, ruleRiskSolution, componentPath, lineStart, snippetStart, snippetEnd, snippet = exeData.getHS()
    if check == 0:
        print(f"Error encountered retreiving data of Hotspot '{currKey}'")
    else:
        time = datetime.now()
        print(f"[{time}] Prompting key '{currKey}' to LLM...")
        exeOpen = getCompletion()
        firstPrompt = PROMPT.format(componentPath = componentPath, lineStart = lineStart, snippet = snippet, ruleRiskDescription = ruleRiskDescription, ruleRiskAssessment = ruleRiskAssessment, ruleRiskSolution = ruleRiskSolution)
        fullMessage = [{"role": "user", "content": PROMPT_Q}, {"role": "assistant", "content": "Understood. I will keep in mind the informations given to me and I will do my best to correctly help you with the analysis."},
                        {"role": "user", "content": firstPrompt}]
        answerLLM = exeOpen.answer(".", FLL_MSG=fullMessage)
        answerCommentLLM = answerLLM.content
        print(f"The LLM answered: {answerCommentLLM}")
        with open("conversationsLog_Hotspots.txt", "a") as lf:
            lf.write(f"[{time}]Conversation Answers\nProject Name: '{project_Name}'\nSecurity Hotspot: '{currKey}':\n\n{answerCommentLLM}\n")
        
        parsedAnswerCommentLLM = answer_parse(answerCommentLLM)
        modelRisk = 0 if "IT IS NOT" in parsedAnswerCommentLLM["RISK"] else 1
        modelHelp = parsedAnswerCommentLLM["I_NEED"] if parsedAnswerCommentLLM["I_NEED"] else "_"
        modelSolution = parsedAnswerCommentLLM["SOLUTION"]
       
        fullMessage = [{"role": "user", "content": PROMPT_Q}, {"role": "assistant", "content": "Understood. I will keep in mind the informations given to me and I will do my best to correctly help you with the analysis."},
                        {"role": "user", "content": firstPrompt}, {"role": "assistant", "content": answerCommentLLM},
                        {"role": "user", "content": PROMPT_VALIDATION}]
        validateLLM = exeOpen.answer(".", FLL_MSG = fullMessage)
        validateCommentLLM = validateLLM.content
        print(f"\nThe LLM answered: {validateCommentLLM}")
        with open("conversationsLog_Hotspots.txt", "a") as lf:
            lf.write(f"\nVALIDATION:\n{validateCommentLLM}\n")
        
        if "yes" not in validateCommentLLM[:8].lower():
            parsedAnswerCommentLLM = answer_parse(validateCommentLLM)
            modelSolution = parsedAnswerCommentLLM["SOLUTION"]
            modelRisk = 0 if "IT IS NOT" in parsedAnswerCommentLLM["RISK"] else 1
            
        if modelSolution == "":
            modelSolution = "Error parsing the .JSON format provided by the LLM"
         
        modelComment = "This is a Risk, here is a Solution provided by the LLM:\n" + modelSolution if modelRisk == 1 else "This is not a Risk according to the LLM."
        print(f"\nSOLUTION:\n{modelComment}")
        with open("conversationsLog_Hotspots.txt", "a") as lf:
           lf.write(f"\nSOLUTION:\n{modelComment}\n--------------------------------------------------------------------------------\n--------------------------------NEW CONVERSATION--------------------------------\n--------------------------------------------------------------------------------\n")
           
        conversationData = {"time": time, "projectName": project_Name, "hotspotKey": currKey, "modelSolution": modelComment}
        log_data = []
        if os.path.exists("logHotspots.json"):
            try:
                with open("logHotspots.json", 'r') as f:
                    log_data = json.load(f)
            except JSONDecodeError:
                print("Error: Invalid JSON format in log file. Starting with an empty log.")
                log_data = []
        log_data.append(conversationData)
        with open("logHotspots.json", 'w') as f:
            json.dump(log_data, f, indent=4, default=str)          
        
        status = postHotspotStatus(key = currKey, resolution = "ACKNOWLEDGED", comment = modelComment)
        status.apply()
        
os.remove(exeJson)