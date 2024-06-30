from variableQuestions import ApplicationServices, InternetExposure, PrivilegeRequirements, EnvironmentManagement, ProtectionConfig, EncryptionPractices, TrustedOrigins, FilePaths

PROMPT = """
You are going to assist with the analysis of a {HSorV}, but before performing any analysis, you are given some informations about the project you are going to analyze.
Here are the Application Services present in the Project and the way they communicate:
{ApplicationServices}
Here is the way the Application is exposed to the Internet:
{InternetExposure}
Here are the Privilege Requirements in the Application:
{PrivilegeRequirements}
Here is how the Environment Variables are managed in the Application:
{EnvironmentManagement}
Here is how the Security Configurations are implemented in the Application:
{ProtectionConfig}
Here are the Encryption Practices adopted for Data Transits happening in the Application:
{EncryptionPractices}
Here are the project Trusted Origins and the way they are managed:
{TrustedOrigins}
Here is an extensive list of File Paths for each file in the Application:
{FilePaths}

Keep these informations in mind while assisting with the analysis of the {HSorV}.
"""

PROMPT_QV = PROMPT.format(HSorV="Security Hotspot", ApplicationServices=ApplicationServices, InternetExposure=InternetExposure, PrivilegeRequirements=PrivilegeRequirements, EnvironmentManagement=EnvironmentManagement, ProtectionConfig=ProtectionConfig, EncryptionPractices=EncryptionPractices, TrustedOrigins=TrustedOrigins, FilePaths=FilePaths)
PROMPT_QHS = PROMPT.format(HSorV="Vulnerability", ApplicationServices=ApplicationServices, InternetExposure=InternetExposure, PrivilegeRequirements=PrivilegeRequirements, EnvironmentManagement=EnvironmentManagement, ProtectionConfig=ProtectionConfig, EncryptionPractices=EncryptionPractices, TrustedOrigins=TrustedOrigins, FilePaths=FilePaths)