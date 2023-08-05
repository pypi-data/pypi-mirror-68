# StreamSQL API

The Python API for StreamSQL enables developers to interact with their StreamSQL instance.
StreamSQL is a unified data pipeline for ML feature engineering and input serving. 
It abstracts batch and streaming data under one interface to allow your ML data scientists to 
add, update, and remove input features using only SQL, Tensorflow, or custom Python functions. 
It works in both training and serving environments and includes stateful storage for ML primitives 
like embeddings, and native integrations into Tensorflow. 


## Getting Started
The StreamSQL Python API provides tools to interact with the Client and Execution environments
of StreamSQL. This includes creating, deleting, and inspecting tables, streams, and transformations, 
as well as data ingestion and retrieval. 

### Requirements

#### Python
StreamSQL API requires Python 3. It has been tested with Python v3.5.

#### StreamSQL
If you haven't already created a StreamSQL instance, you can signup and create one 
[here](https://streamsql.io)

### Installing
You can install the StreamSQL API with pip

```
pip install streamsql
```

## Usage
Below are some example use cases for the StreamSQL API

### Examples


#### Sending Data
```python
from streamsql import SimpleClient

# Create a Client object to interact with the client environment
client = SimpleClient(APIKEY)

# Example Event
event = {
    "user": {
        "first_name": "John",
        "last_name": "Smith",
        "username": "john_smith"
    },
    "action": "Login",
    "timestamp": "2020-02-20T21:39:18+00:00"
}

# Put the event into an immutable data stream
client.send('MyStream', event)

# Fetch the last login of "john_smith" from a lookup table
client.lookup('LastLogin', 'john_smith')

```

#### Transforming Data

```python
from streamsql import SimpleClient, FieldTypes

# Create a Execution object to interact with the execution environment
exc = SimpleClient(APIKEY)

# Register a stream named "MyStream"
exc.create_stream("MyStream").commit()

# Register a lookup named "LastLogin"
(
exc.create_lookup("LastLogin")
    .source("MyStream")             # Set the data source and type
    .extract("user.username", "username", "STRING")   # Extract a field from the JSON object and provide an alias and type  
    .extract("timestamp", "ts", "TIMESTAMP")          
    .query("SELECT username, ts FROM MyStream")                             # Use SQL query to generate results
    .commit()
)

```









