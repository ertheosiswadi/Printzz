# Flask Server Backend
This folder contains the backend and frontend code for the flask server as well as the frontend.
The server is currently being hosted at [printzz.herokuapp.com](https://printzz.herokuapp.com)

## Project Structure

The Server is laid out such that Heroku can run and host this server easily. Heroku needs the app.py, the Procfile, and the runtime.txt to know how to run the server. The entire structure is setup to allow Heroku to easily start up and run the server correctly

### Flask Server Source Code

The source code for the flask server is located directly in the src/ directory. Besides the python source code, static HTML, CSS, and JavaScript is also included to send to the Frontend

### Frontend Code

The frontend code is stored within the static and templates folders within the src/ directory

## Setup

Create your python virtual environment.
```
python -m venv ENV
```

Activate your virtual environment
```
source ENV/bin/active
```

Install the required modules
```
pip install -r requirements.txt
```

## Running the server locally

To run the server locally, just run the file locally
```
python server.py
```
