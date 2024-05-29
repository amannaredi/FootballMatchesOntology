# Football Matches Ontology Project

This repository contains the implementation and analysis of a Football Matches Ontology. The project includes ontology design, population from multiple data sources, querying, and reasoning using SWRL rules.

## Table of Contents
- [Introduction](#introduction)
- [Core Task](#core-task)
- [Extra Task](#extra-task)
- [Advanced Task](#advanced-task)
- [Source Code and Execution](#source-code-and-execution)
- [References](#references)

## Introduction
The Football Matches Ontology aims to provide a structured representation of information related to football matches, competitions, teams, and stadiums. The ontology facilitates match league analysis, stadium analysis, and various other applications within the sports domain.

## Core Task
### Objective
To design an ontology that captures the essential aspects of football matches, including matches, competitions, teams, and stadiums.

### Ontology Design
The ontology uses OWL2 for defining the structure and relationships. Main classes include:
- **Match**
- **Competition**
- **Stadium**
- **Team**

### Population and Querying
Data is populated from DBpedia and queried using SPARQL.

## Extra Task
### Objective
To enhance the ontology with additional data from WikiData and non-semantic data sources.

### Data Population
- **WikiData**: Used to obtain additional details such as match class and winning team.
- **CSV Integration**: Non-semantic data from a CSV file is converted to RDF and integrated into the ontology.

### Querying
The integrated data is queried to answer complex questions that DBpedia alone could not resolve.

## Advanced Task
### Objective
To implement SWRL rules and reasoners to derive meaningful inferences from the ontology.

### SWRL Rules
- **High Scoring Match**: Identifies matches with more than 3 goals.
- **Large Stadium**: Identifies stadiums with a capacity greater than 50,000.
- **Popular Match**: Identifies matches with more than 50,000 attendees.

## Source Code and Execution
The repository includes Python scripts for ontology population, querying, and integration:
- `basicTask_dbpedia_dataLoad.py`: Populates data from DBpedia.
- `extraTask_wikiData_Load.py`: Populates data from WikiData.
- `non_semanticload.py`: Populates data from a CSV file.
- `basicTaskquery_localStore.py`: Queries the local ontology populated by DBpedia.
- `extraTaskquery_localStore.py`: Queries the local ontology after integrating WikiData and CSV data.

### Commands
To set up and run the project, follow these commands:

```sh
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Load data from DBpedia
python basicTask_dbpedia_dataLoad.py

# Load data from WikiData
python extraTask_wikiData_Load.py

# Load data from CSV
python non_semanticload.py

# Query local ontology populated by DBpedia
python basicTaskquery_localStore.py

# Query local ontology after integrating WikiData and CSV data
python extraTaskquery_localStore.py
```
