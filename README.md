# Python Django Assignment

## Local Setup

1) Clone the repository and cd into it.

2) Create a virtual environment and activate it through following commands in the root dir:
```
python3 -m venv .venv
source .venv/bin/activate
```
3) run the command `make setup` to install dependencies and create .env file

4) open .env file and add the MongoDB connection string and also the name of the database.

5) Now to run the backend server, simply type make runserver to initiate the server at http://127.0.0.1:8000/

6) Use the urls mentioned in the assignment, namely
 - `accounts/register/`,
 - `accounts/login/`,
 - `accounts/profile/view`,
 - `accoutns/profile/edit`,

 7) Hit the APIs with using Postman or curl requests and you should get the appropriate responses.

 8) The JWT token must be sent through `Custom-Token` header in the request.

 9) After login, the custom token is sent under `Authorization` key in the response
