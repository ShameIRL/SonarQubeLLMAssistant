def answer_parse(answerText):
    segments = {"ASSESSMENT": "", "RISK": "", "SOLUTION": "", "I_NEED": ""}
    
    start = answerText.find('"ASSESSMENT":')
    end = answerText.find('"RISK":')
    if start != -1 and end != -1:
        segments["ASSESSMENT"] = answerText[start + len('"ASSESSMENT":'):end].strip().rstrip(',')
    
    start = end
    end = answerText.find('"SOLUTION":')
    if start != -1 and end != -1:
        segments["RISK"] = answerText[start + len('"RISK":'):end].strip().rstrip(',')
    
    start = end
    end = answerText.find('"I_NEED":') if '"I_NEED":' in answerText else -1
    if start != -1 and end != -1:
        segments["SOLUTION"] = answerText[start + len('"SOLUTION":'):end].strip().rstrip(',')
    
    start = end
    if start != -1:
        segments["I_NEED"] = answerText[start + len('"I_NEED":'):].strip().rstrip(',')
    
    return segments