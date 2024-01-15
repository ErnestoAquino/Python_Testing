
# gudlift-registration

## Why
This is a proof of concept (POC) project to demonstrate a lightweight version of our competition booking platform. The goal is to keep things as lightweight as possible and use user feedback to iterate.

## Getting Started
This project uses the following technologies:
- Python v3.x+
- Flask
-  pytest
- locust
- flake8
- coverage


While Django does a lot for us by default, Flask allows us to add only what we need.
### Naming Convention

In this project, we follow the snake_case naming convention.

### Virtual Environment
This ensures you can install the correct packages without interfering with Python on your machine. Please make sure you have this installed globally before starting.

## Installation
First, clone the repository with the command:

```bash
git clone https://github.com/ErnestoAquino/Python_Testing.git
```

Navigate to the folder:

```bash
cd Python_Testing
```

Create a virtual environment:

```bash
python3 -m venv env
```

Activate the virtual environment:

```bash
source env/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Set the Environment Variable:

```bash
export FLASK_APP=server.py
```

Now you can run the application with the command:

```bash
flask run
```

## Current Setup
The application is powered by JSON files. This is to avoid having a database until we actually need one. The main ones are:
- `competitions.json` - list of competitions
- `clubs.json` - list of clubs with relevant information. You can check here which email addresses the application will accept for login.

### Viewing Club Points
To check the available points of clubs, you do not need to be logged in. You can access the following route:

```bash
/club-points
```

## Testing
You can run the tests with the following command:

```bash
pytest --cov=.
```

To generate a report, you can use the following command:

```bash
pytest --cov=. --cov-report html
```

This will generate a folder called `htmlcov`. You can open the `index.html` file to view the results.

## Performance Tests
The performance test uses two json files with test data so as not to affect the real json files during the test.

To run the performance test, you need to make sure the server is stopped and set the environment variable:

```bash
export FLASK_ENV=testing
```

Now restart the application:

```bash
flask run
```

In another terminal, go to the Python_Testing repository folder and run the script using the following command:

```bash
locust -f tests/performances_tests
```

You can open the web interface and configure 6 users, run the test for 3 minutes in the run time field, and start the test.

Once the test is finished, you can stop locust with ctrl + c and view the results.
