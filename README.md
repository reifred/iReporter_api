[![Build Status](https://travis-ci.com/reifred/ireporter_api.svg?branch=develop)](https://travis-ci.com/reifred/ireporter_api)
[![Coverage Status](https://coveralls.io/repos/github/reifred/ireporter_api/badge.svg?branch=develop)](https://coveralls.io/github/reifred/ireporter_api?branch=develop)
# ireporter_api
## Description
iReporter is an application that enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.
It was developed because corruption is a huge bane to Africa's development.

## Getting Started
Follow these instructions to get a copy of the API to run on your machine.

### Prerequisites

Install the following programs before using the API:
```
1. Python version 3.7.1
2. Postman
```

### Instructions for set up

- Clone into this repo using:
```
git clone https://github.com/reifred/ireporter_api.git
```
- Set up a virtual environment for python in the project directory
- Install the required packages using:
```
pip install -r requirements.txt
```
### Running the tests

Use the following command to run the tests in your virtual environment:
```
pytest -v
```

### Running the application
Use the following command in the project folder to run the app:
```
python run.py
```

### End points
 HTTP method|End point|functionality 
 -----------|---------|--------------
 GET|/|A welcome route to the application
 GET|/api/v1/red_flags/| Return all red-flags available
 GET|/api/v1/red_flags/<red_flag_id>| Used to get a specific red-flag record's details.
 POST|/api/v1/red_flags| Used to create a red-flag record
 PATCH|/api/v1/red_flags/<red_flag_id>/location| Used to edit the location of a given red-flag record 
 PATCH|/api/v1/red_flags/<red_flag_id>/comment| Used to edit the comment of a given red-flag record
 DELETE|/api/v1/red_flags/<red_flag_id>| Used to delete a specific red-flag record 
 
 ### Built with
 * [Flask](http://flask.pocoo.org/) - micro web framework for Python
 * [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create a virtual environment
 * [PIP](https://pip.pypa.io/en/stable/) - A python package installer

## Tools Used
* Pivotal Tracker used to user stories for this project
* Visual Studio acting as an editor for the project files 
* Github
* Postman used to test the api end points

## Deployment
The link to ***Heroku*** where the api is deployed [here](https://fred-ireporter-api.herokuapp.com/)
Append the api end points stated above to this home route.

  ### Authors
Mugerwa Fred
