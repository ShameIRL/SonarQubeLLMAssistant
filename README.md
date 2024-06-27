# SonarQube Large Language Model Assistant

[![SonarQube 10.5 Community](https://img.shields.io/badge/SonarQube-10.5_Community-004d80.svg)](https://www.sonarsource.com/products/sonarqube/downloads/historical-downloads/)
[![SonarScanner CLI 5.0.1](https://img.shields.io/badge/SonarScanner_CLI-5.0.1-004d80.svg)](https://docs.sonarsource.com/sonarqube/10.5/analyzing-source-code/scanners/sonarscanner/)
[![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/downloads/release/python-3123/)
![openai 1.30.1](https://img.shields.io/badge/openai-1.30.1-blue.svg)
![requests 2.31.0](https://img.shields.io/badge/requests-2.31.0-blue.svg)

> [!NOTE]
> The content of this Repository is not guaranteed to work with versions differing from the ones listed above; \
> Future versions might work as well but there is no guarantee.

## Table of Contents

+ [About](#about)
+ [Getting Started](#gettingStarted)
    + [SonarQube \& SonarScanner Installation](#sonarInstall)
    + [SonarQube Prerequisites](#sonarPrerequisites)
    + [Large Language Models Prerequisites](#largeLanguageModelsPrerequisites)
    + [Python \& Libraries Prerequisites](#pythonPrerequisites)
+ [Execution](#execution)
    + [Variables Definition](#variablesDefinition)
    + [Security Hotspots Analysis](#securityHotspotEXE)
    + [Vulnerabilities Analysis](#vulnerabilityEXE)
  
## About <a name = "about"></a>

This Repository contains the experimental solution produced during an Internship at [_Zucchetti S.p.A._](https://www.zucchetti.com/worldwide/cms/home.html), which aimed to study the capabilities of small size _Large Language Models_ (range 3B to 8B) and test various techniques to improve them. The practical application context of this experimental study was _Static Analysis Softwares_, specifically the _SonarQube_ platform. \
The solution produced automatically obtains the project reports related to _Security Hotspots_ and _Vulnerabilities_ from _SonarQube_. A _Large Language Model_ then automatically performs the analysis of each report. Eventually it automatically changes the status of the analyzed report, discarding false positives, and adds a comment containing a possible solution. \
The below [_Getting Started_](#gettingStarted) section defines how to setup the _SonarQube_ platform and lists a series of prerequisites necessary to the execute the solution, while the [_Execution_](#execution) section explains how to properly execute this experimental solution.

## Getting Started <a name = "gettingStarted"></a>

### SonarQube \& SonarScanner Installation <a name = "sonarInstall"></a>

> [!IMPORTANT]
> Please note that the external links may change and not be reachable in the future; \
> Also note that the links redirecting to the _SonarQube_ documentation are related to _SonarQube 10.5_. To change version select it from the top-left drop down version menu.

_SonarQube_ installation is straight forward and it can be downloaded [_here_](https://www.sonarsource.com/products/sonarqube/downloads/historical-downloads/). \
_SonarQube_ requires _SonarScanner_ to perform project analyses. _SonarScanner_ has different editions, during the Internship the projects that were analyzed where locally stored, so _SonarScanner CLI_ was used. _SonarScanner CLI_ installation is straight forward and it can be downloaded [_here_](https://docs.sonarsource.com/sonarqube/10.5/analyzing-source-code/scanners/sonarscanner/) from the _SonarQube_ documentation section. \
Additional detailed information about the platfrom are found in the platform's [_documentation_](https://docs.sonarsource.com/sonarqube/10.5/).

### SonarQube Prerequisites <a name = "sonarPrerequisites"></a>

The _SonarQube_ platform needs to be running for the projects to be created and for the scripts to work. \
To start the _SonarQube_ platform the command is:

- Linux:
``` bash
$ cd path/to/sonarqube/folder
$ bin/linux-x86-64/sonar.sh console
```
- macOS:
``` bash
$ cd path/to/sonarqube/folder
$ bin/macosx-universal-64/sonar.sh console
```
- Windows:
``` bash
$ cd path\to\project\base\folder
$ bin\windows-x86-64\SonarService.bat console
```
To run the scripts a project must exist in the _SonarQube_ platform. The project needs to have been analyzed by _SonarScanner_. \
The analysis is performed during the creation process of a _SonarQube_ project. After selecting some project variables _SonarQube_ displays a command to execute the analysis through _SonarScanner_. The following command performs the analysis of a locally stored project, project specific variables between angle brackets:

- Linux \& macOS:
``` bash
$ cd path/to/project/base/folder
$ sonar-scanner \
    -Dsonar.projectKey=<projectName> \
    -Dsonar.sources=. \
    -Dsonar.host.url=<sonarQubeURL> \
    -Dsonar.token=<projectAnalysisToken>
```
- Windows:
``` bash
$ cd path\to\project\base\folder
sonar-scanner.bat -D"sonar.projectKey=<projectName>" -D"sonar.sources=." -D"sonar.host.url=<sonarQubeURL>" -D"sonar.token=<projectAnalysisToken>"
```
At least one _Security Hotspot_ or _Vulnerability_ has to be detected in the project. To check their presence the user needs to navigate to the _Security Hotspots_ section in the first case, while for the latter the user needs to navigate in the _Issues_ section and then select the _Vulnerability_ type. Their presence can also be easily checked through the project's card in the _SonarQube_ projects main page, checking for _Security_ and _Hotspots_.

### Large Language Models Prerequisites <a name = "largeLanguageModelsPrerequisites"></a>

> [!TIP]
> The bigger the _Large Language Model_ the better the performance should be, avoid quantized models; \
> _StarlingLM ExPO_ is suggested for limited hardware devices, as per best benchmark results; \
> _LM Studio_ is suggested to run the _Large Language Model_ due to its easy usability.

To run the scripts a _Large Language Model_ needs to be loaded in a server that can be contacted through _OpenAI APIs_. \
This solution was mainly tested with single _Large Language Model_ servers, however servers that can run multiple _Large Language Models_ are supported as well.

### Python \& Libraries Prerequisites <a name = "pythonPrerequisites"></a>

_Python_ is required, along with the _openai_ and _requests_ libraries. \
The versions used in the development are _Python 3.12.3_, _openai 1.30.1_ and _requests 2.31.0_, however any version should work.

## Execution <a name = "execution"></a>

### Variables Definition <a name = "variablesDefinition"></a>

Before executing the scripts a series of variables must be specified in the following files:
- _"variables.py"_ contains specific variables related to the _SonarQube_ and the _Large Language Model_ servers.
- _"variableQuestions.py"_ contains the answers to specific questions that will allow the _Large Language Model_ to perform the analysis better, due to additional context.

Edit the above files by adding the information required by the comments related to each variable before running the scripts.

### Security Hotspots Analysis <a name = "securityHotspotEXE"></a>

Once the [prerequisites](#gettingStarted) are respected, the analysis of _Security Hotspots_ can be performed by simply executing the _"executeHS.py"_ file:
- Linux \& macOS:
``` bash
$ cd path/to/the/execute/file
$ python3 executeHS.py
```
- Windows:
``` bash
$ cd path\to\the\execute\file
$ python executeHS.py
```
This execution analyzes the selected project's _Security Hotspots_ and edits their statuses on the _SonarQube_ platform, while adding a comment containing the _Large Language Model_'s resolution. \
A _"conversationsLog_Hotspots.txt"_ file is created to keep track of all the conversations with the _Large Language Model_ in their entirety, while a _"logHotspots.json"_ file tracks the solutions provided by the _Large Language Model_ for each analyzed _Security Hotspot_.

### Vulnerabilities Analysis <a name = "vulnerabilityEXE"></a>

Once the [prerequisites](#gettingStarted) are respected, the analysis of _Vulnerabilities_ can be performed by simply executing the _"executeV.py"_ file:
- Linux \& macOS:
``` bash
$ cd path/to/the/execute/file
$ python3 executeV.py
```
- Windows:
``` bash
$ cd path\to\the\execute\file
$ python executeV.py
```
This execution analyzes the selected project's _Vulnerabilities_ and edits their statuses on the _SonarQube_ platform, while adding a comment containing the _Large Language Model_'s resolution. \
A _"conversationsLog_Vulnerabilities.txt"_ file is created to keep track of all the conversations with the _Large Language Model_ in their entirety, while a _"logVulnerabilities.json"_ file tracks only the solutions provided by the _Large Language Model_ for each analyzed _Vulnerability_.
