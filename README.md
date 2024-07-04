# The Dancing Pony

The Dancing Pony is a FastAPI application that manages user authentication and allows CRUD operations on a collection of dishes. It uses HTTP Basic Authentication and includes mechanisms to temporarily block users after multiple failed login attempts.

## Features

- User registration and authentication
- CRUD operations for dishes
- Basic HTTP authentication
- Temporary blocking of users after multiple failed login attempts

## Installation

1. **Clone the repository:**

```sh
   git clone https://github.com/yourusername/the-dancing-pony.git
   cd the-dancing-pony
```

2. **Set up virtual environment and install dependencies**
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set up PostgreSQL**

Create a database called `dancingpony`:
```sh
sudo -u postgres psql
CREATE DATABASE dancingpony;
CREATE USER dancingponysvc WITH PASSWORD 'password';
ALTER ROLE dancingponysvc SET client_encoding TO 'utf8';
ALTER ROLE dancingponysvc SET default_transaction_isolation TO 'read committed';
ALTER ROLE dancingponysvc SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dancingpony TO dancingponysvc;
```

Then, run the `run_create_schemas.py` file in the `db` directory:
```sh
python db/run_create_schemas.py
```

This will create the tables for the dish and user entities. Next, insert some dummy data into the dish table:
```sh
python db/insert_data.py
```

This will insert dishes in the table that can be used for querying. 

## Running the Application
1. **Start the service**
```sh
python -m uvicorn main:app --reload
```

2. **Access API endpoints**
Since the application was built in FastAPI, the Swagger UI is available by default. Navigate to:
```sh
http://localhost:8000/docs
```

From here, all the routes of the application should be available, including ways to test them. 