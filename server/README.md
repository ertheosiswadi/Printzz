# Flask Server Backend
This folder contains the backend code for the flask server.


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

## Running the server

To run the server locally, just run the file locally
```
python server.py
```

## EndPoints

NOTE: For every endpoint, if the response is a json object, it will always be structured as follows

```
{
    "status": bool,
    "data": {
        // Data
    }
}
```

### `register`

The `register` endpoint is used to register a user.

#### `POST`

The `POST` register endpoint provides the ablility to register a user in the server.

##### Request

To register a user, just call this method with json data as follows
```
{
    "username": "example_name",
    "password": "example_password"
}
```

##### Response

In response, the API will do one of two things.

If the username already exists in the system, this call will return a json object with a status flag that is false

I the username does not exist, the status flag will be true and the json object returned will look like follows

```
{
    "status": true,
    "data": {
        "username": "example_name",
        "user_id": "random_string"
    }
}
```

### `login`

The login endpoint is used to receive the user_id for the username provided

#### `POST`

##### Request

To request the user_id for a user, send a json object structured as follows
```
{
    "username": "example_name",
    "password": "example_password"
}
```

##### Response

If the username and password match an entry in the server, it will return an object as follows
```
{
    "status": true,
    "data": {
        "username": "example_name",
        "user_id": "random_string"
    }
}
```

Otherwise, it will return a json object with a false status flag

### `add_doc_file`

#### `POST`

Uploads document to server.

NOTE: this does not add the file to the queue.
`add_doc_settings` must be called AFTER `add_doc_file` to actually add the document to the queue

##### Request

For the `add_doc_file` endpoint, the `user_id` must be included as a param. Then, the file will be uploaded through a mutlipart form in the field titled `input_file`

example:
```
https://printzz.herokuapp.com/add_doc_file?user_id=AUTH_KEY
```

##### Response

Returns a json object with a false status flag if the `user_id` provided is not valid

Otherwise, return json object with a true status flag

### `add_doc_settings`

#### `POST`

Applies settings passed in to the document uploaded last for the user by `add_doc_file`

NOTE: Must be called after a file was uploaded with `add_doc_file`

##### Request

`user_id` must be included as a parameter as with the `add_doc_file` endpoint

json must also be included with the settings for the document. This is shown below:
```
{
    "double_sided": true,
    "copies": 1,
    "color": true
}
```

##### Response

if the `user_id` provided is not valid, this endpoint will return false

Otherwise, if a document has not be uploaded yet, it will also return false

If a document has been uploaded, the document will be added to the print queue and json show below will be returned
```
{
    "status": true,
    "data": {
        "username": "example",
        "user_id": "random_string",
        "doc_name": "document_name,
        "ext": "extension, such as pdf",
        "doc_id": "random_string",
        "settings": {
            "double_sided": true,
            "copies": 1,
            "color": true
        },
        "progress": 0
    }
}
```

### `get_doc`

#### `GET`

Returns the document on the top of the queue

##### Request

No request data needed

##### Response

Returns the top most document of the queue. If the queue is empty, returns a json object with a false status flag

### `get_doc_settings`

#### `GET`

Returns the settings of the document on the top of the queue

##### Request

No request data needed

##### Response

If queue is empty, returns json object with a false status flag

Otherwise, returns the settings of the top most document in an object shown below
```
{
    "status": true,
    "data": {
        "double_sided": true,
        "copies": 1,
        "color": true
    }
}
```

### `pop_doc`

#### `GET`

Pops the top doc off the queue

##### Request

No request data needed

##### Response

Returns status flag of true if queue isnt empty, returns false otherwise
