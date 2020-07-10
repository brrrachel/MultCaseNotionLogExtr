# MultCaseNotionLogExtrThis repository hosts all data for our project in the Data Extraction for Process Mining Seminar Project by Rachel Brabender and Oliver Clasen.## Setup PythonWe are using some libraries which are not part of the normal python libraries. Therefore, we wrote a setupFile which will install those.```bash installLibraries.sh```## Run Process SimulatorThe code below executes our self-written process simulator which creates the sortedTableLog.csv file as a basis for the different case notion extractions.```python3 process_simulator.py```## Run XES Log Extractor```python3 xes_log_tool.py```