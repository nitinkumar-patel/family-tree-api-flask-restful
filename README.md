# Family Tree API Using Flask

*Coding Challenge to create a Family Tree API using Flask, SQLAlchemy and pytest.*

## Instructions

### Installation Process
1. `git clone` repo

##### Create virtual environment

if you want to create virtual environment and install pipenv in created python virtual env

```bash
virtualenv -p python3.7 python_env
```
OR
```bash
pip3 install virtualenv
python3.7 -m virtualenv python_env
source python_env/bin/activate
pip install pipenv

```

To deactivate virtual python_env
```bash
deactivate
```

##### Running the service in a virtual environment
If you are using python 3.7 you will need to run
```bash
pipenv run pip install pip==18.0
```

To install dependencies you will need to run
```bash
pipenv install
```

Once dependencies are installed you can run the service with
```bash
pipenv run python manage.py runserver
```

positional arguments:
  {runserver,db,shell}
    runserver           Runs the Flask development server i.e. app.run()
    db                  Perform database migrations
    shell               Runs a Python shell inside Flask application context.



To run test cases (pytest)
```bash
pipenv run pytest
```

test-pdb
```bash
pipenv run pytest --pdb
```

To check test coverage
```bash
pipenv run pytest --cov
```

To generate test coverage report in html
```bash
pipenv run pytest --cov --cov-report html && open ./htmlcov/index.html
```


# be-coding-challenge

### Expectations
- We do not expect you to completely finish the challenge. We ask that candidates spend 4 hours or more working through the challenge. With that we understand that everyones schedule and availability is different so we ask that you provide a reasonable estimate of your time commitment so we can take it into account when evaluating your submission.
- We expect you to leverage creative license where it makes sense. If you'd like to change the project structure, pull in libraries, or make assumptions about the requirements we openly encourage you to do so. All that we ask is that you are prepared to talk about your choices in future interviews. 

### Challenge
For this challenge you will be implementing a family tree API.

The API should be capable of keeping track of people and the connections between them.

While you have full control to model the entities as you see fit you should keep the following guidelines in mind.

Details about a person and their relationships should be editable. At a minimum you should use the following traits to describe a person: 
- First name
- Last name
- Phone number
- Email address
- Address
- Birth date

When thinking about relations between people the API should be able to provide the following information
- For a given person list all of their siblings
- For a given person list all of their parents
- For a given person list all their children
- For a given person list all of their grandparents
- For a given person list all of their cousins


## API Endpoints

### `/api/v1/persons/`

- *GET*
- *POST*

### `/api/v1/persons/{person_id}`

- *GET*
- *PUT*
- *DELETE*

### `persons/{person_id}/siblings`

- *GET*

### `persons/{person_id}/parents`

- *GET*

### `persons/{person_id}/children`

- *GET*

### `persons/{person_id}/grandparents`

- *GET*

### `persons/{person_id}/cousins`

- *GET*

### `persons/?page={page_no}`

- *GET*

### `persons/?firstname={first_name}`

- *GET*

### `persons/?state={state}`

- *GET*

### `persons/?firstname={first_name}&state={state}`

- *GET*




## Resources

- [Flask Docs: App Factories](http://flask.pocoo.org/docs/1.0/patterns/appfactories/)
- [Flask Mega Tutorial: App Factories](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)
- [Genealogy Data Model](http://www.databaseanswers.org/data_models/genealogy/index.htm)
