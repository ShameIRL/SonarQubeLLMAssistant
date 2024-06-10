PROMPT_JSON = """
A Vulnerability is a flaw or weakness in the software that can be exploited by an attacker to compromise the system's security.
Some Vulnerabilities are not real and might be false positives.

- This is a code snippet from {componentPath} where a Vulnerability appears in line {lineStart}:
CODE SNIPPET:
{snippet}
The Vulnerability above happens because {ruleName}.
- This is the description of the Vulnerability:
VULNERABILITY DESCRIPTION:
{ruleDescription}
- The cause of this Vulnerability is:
VULNERABILITY CAUSE:
{ruleCause}
- This is the way to fix the Vulnerability:
SOLUTION:
{ruleSolution}

You must now analyze the CODE and based on the VULNERABILITY DESCRIPTION and on the VULNERABILITY CAUSE you must decide if this is a false positive.
If this is an actual risk you must provide a SOLUTION, otherwise you must communicate that the vulnerability was a False Positive. Always proceed step by step.

Provide the answer EXCLUSIVELY in .JSON format, the content has to be as follows:
- "RISK": "IT IS a risk."/"IT IS NOT a risk, it is a FALSE POSITIVE."
- "SOLUTION": "Your provided SOLUTION, which has to fix the original code."
"""

PROMPT_VALIDATION = "Are the above risk and solution CORRECT? If the answer is positive EXCLUSIVELY say \"YES\", always provide the corrected .JSON."