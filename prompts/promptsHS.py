PROMPT_JSON = """
A Security Hotspot highlights a security-sensitive piece of code that must be reviewed. Upon review, it will either be found that it is safe or that a fix must be applied to secure the code.

- This is a code snippet from {componentPath} where a Security Hotspot appears in line {lineStart}:
CODE SNIPPET:
{snippet}
- This is the POSSIBLE risk of the above Security Hotspot:
HOTSPOT DESCRIPTION:
{ruleRiskDescription}
- This is the way to assess whether the risk is real or false:
RISK ASSESSMENT:
{ruleRiskAssessment}
- This is the way to fix the Security Hotspot if it is an actual risk:
SOLUTION:
{ruleRiskSolution}

You must now to analyze the CODE and based on the HOTSPOT DESCRIPTION, you must perform a RISK ASSESSMENT considering the software context.
If you find an actual risk you must provide a SOLUTION, otherwise you must communicate that there is no risk. Always proceed step by step.

Provide the answer EXCLUSIVELY in .JSON format, the content has to be as follows:
- "ASSESSMENT": "The questions and your answers to the step by step ASSESSMENT."
- "RISK": "IT IS a risk."/"IT IS NOT a risk."
- "SOLUTION": "Your provided SOLUTION, which has to fix the original code."
"""

PROMPT_VALIDATION = "Are the above assessment, risk and solution CORRECT? If the answer is positive EXCLUSIVELY say \"YES\", always provide the corrected .JSON."