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

## Instructions for set up
- Clone into this repo using:
```
git clone https://github.com/reifred/ireporter_api.git
```
### Set up a virtual environment for python in the project directory
Inorder to set up the virtual environment, you need to install the python package called virtualenv using pip.
Run the command below to install it.
- `pip install virtualenv` to install virtualenv
- `virtualenv virtual`  to create a virtual environment named virtual
- `virtual/Scripts/activate` to activate your virtual environment.
- `virtual/Scripts/deactivate` to deactivate your virtual environment.

### Install the required packages using:
After setting up and activating your virtual environment, you need to install all the packages required by the project.
```
pip install -r requirements.txt
```
### Running the tests

Use the following command to run the tests in your virtual environment:
```
pytest -v
pytest --cov to see coverage
```

### Running the application
Use the following command in the project folder to run the app:
```
python run.py
```

### End points
 |HTTP method|End point|Functionality| 
 |-----------|---------|--------------|
 |GET|/api/v1/|A welcome route to the application|
 |GET|/api/v1/users|Return all registered users|
 |GET|/api/v1/red_flags|Return all red-flags available|
 |GET|/api/v1/red_flags/int:red_flag_id|Get a specific red-flag record|
 |POST|/api/v1/red_flags|Create a red-flag record|
 |POST|/api/v1/auth/sign_up|Register a new user|
 |POST|/api/v1/auth/sign_in|Login a user or admin|
 |PATCH|/api/v1/red_flags/int:red_flag_id/location|Edit location of specific red-flag record| 
 |PATCH|/api/v1/red_flags/int:red_flag_id/comment|Edit comment of specific red-flag record|
 |PATCH|/api/v1/red_flags/int:red_flag_id/status|Edit status of specific red-flag record|
 |DELETE|/api/v1/red_flags/int:red_flag_id|Delete specific red-flag record|
 
 #### Sample Data to use in postman
```
Registering a user.
{
	"firstname": "Mugerwa",
	"lastname": "Fred",
	"othernames": "",
	"email": "rei@gmail.com",
	"phoneNumber": "0757605424",
	"username": "username",
	"password": "Password123"
}

User Log In.
{
	"username": "username",
	"password": "Password123",
	"isAdmin": false
}

Creating a red_flag
{
	"comment": "New comment about corruption",
	"_type": "red-flag",
	"images": "image.jpg",
	"location": "Lat 11231 Long 14224",
	"videos": "vid.mp4"
}

``` 

#### Sample output after user sign in
```
{
    "data": [
        {
            "id": 1,
            "message": "User login",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImFkbSI6MCwiZXhwIjoxNTQ3Njg2NDQ3fQ.L1aiR6FHeG5vCvsuBFqpZlX4mYaXA845mEL_kvzQ7MY",
            "username": "username"
        }
    ],
    "status": 201
}
```
#### Adding Token to headers using Postman
- In Postman, select an API method.
- Click the Authorization tab.
- Choose OAuth 2.0 or Bearer Token.
- Copy the token above and paste it in the edit text box provided on the right hand side.

 ### Built with
 - [Flask](http://flask.pocoo.org/) - Micro web framework for Python
 - [PIP](https://pip.pypa.io/en/stable/) - A python package installer

## Tools Used
- Pivotal Tracker used to write user stories for this project
- Visual Studio acting as an editor for the project files 
- Github
- Postman used to test the api end points

## Deployment
- The link to ***Heroku*** where the api is deployed [here](https://fred-ireporter-api.herokuapp.com/).
- To access other routes append the api end points stated above to the home route.

  ### Authors
Mugerwa Fred
