[![Build Status](https://travis-ci.com/reifred/ireporter_api.svg?branch=develop)](https://travis-ci.com/reifred/ireporter_api)
[![Coverage Status](https://coveralls.io/repos/github/reifred/ireporter_api/badge.svg?branch=develop)](https://coveralls.io/github/reifred/ireporter_api?branch=develop)
# ireporter_api
## Description
iReporter is an application that enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.
It was developed because corruption is a huge bane to Africa's development.

#### Getting Started
Clone the project using the [link](https://github.com/reifred/ireporter_api.git)

##### Accessing the frontend of the application

## Features

1. Users can create an account with iReporter.
2. User can log in.
3. Users can create a red-flag record to bring any form of corruption to notice.
4. Users can create an intervention to call for government intervention.
5. Users can edit the red-flag or intervention details
6. Users can delete their red-flag or intervention records.
7. Users can add geolocation (Lat Long Coordinates) to their red-flag or intervention records.
8. Users can change the geolocation (Lat Long Coordinates) attached to their red-flag or intervention records.
9. Admin can change the status of a record to either under investigation, rejected (in the event of a false claim) or resolved (in the event that the claim has been investigated and resolved).

# Optional Features
* Users can add images to their red-flag or intervention records, to support their claims.
* Users can add videos to their red-flag or intervention records, to support their claims.
* The application should display a Google Map with Marker showing the red-flag or intervention location.
* The user gets real-time email notification when Admin changes the status of their record.

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
* Pivotal Tracker
* Visual Studio
* Github

## Deployment
The link to ***Heroku*** where the api is deployed [here](https://fred-ireporter-api.herokuapp.com/)

  ### Authors
Mugerwa Fred

