# Python Django Assignment

- This app is made using Django, DjangoRestFramework, and MongoDB

- To connect MongoDB with Django, I have used `Pymongo`.

- Since Django doesn't support NoSQL inherently, there aren't any models or django ORM being used anywhere.

- A direct connection to the MonogoDB is made and collections are used.

- The application uses the `ApiView` class from the django-rest-framework to have a better control over the backend api endpoints and responses.

- Used poetry for seamless dependency management and strict enforcement of Python 3.9 version and Django 3.2.

- Used Makefile for efficient local setup and deployment and to reduce commands.
## Local Setup

1) Clone the repository and cd into it.

2) Create a virtual environment and activate it through following commands in the root dir:
```
python3 -m venv .venv
source .venv/bin/activate
```
3) run the command `make setup` to install dependencies and create .env file

4) open .env file and add the MongoDB connection string and also the name of the database.

5) Please also add a `serviceAccountKey.json` in `bewyse_assignment/src/`. This json file is generated in the firebase console, under project settings, inside service accounts. Use the Generate Private key button to download the json file.

6) Now to run the backend server, simply type make runserver to initiate the server at http://127.0.0.1:8000/

7) Use the urls mentioned in the assignment, namely
 - `accounts/register/`,
 - `accounts/login/`,
 - `accounts/profile/view`,
 - `accounts/profile/edit`,

 8) Hit the APIs with using Postman or curl requests and you should get the appropriate responses.

 9) The JWT token must be sent through `Custom-Token` header in the request.

 10) After login, the custom token is sent under `Authorization` key in the response.

 11) When using `accounts/profile/edit`, provide `username` to reference the record in db, and to change username, provide the new username using `new_username` key in the request.


# Challenges Faced

1) Since I had never worked with Firebase or used it's services, trying to figure it was a rough initially. I was went in circles in trying to figure out how to use firebase for the task mentioned, since there was more coverage about other auth services firebase provides.

    - Eventually I was able to figure out how to generate custom tokens and send it in the response, also had to set up firebase-admin.
    - Mistakenly used verify_id_token() api of firebase api which led to discovering how JWT tokens actually work, and that to verify them we will need to use a JWT library, a public key, and an algorithm
    - I have used PyJwt for this purpose.
    - JWT when decoded reveals the payload which can be and `kid`(key-id) which can be used check if the JWT is valid or not and also the uid used to make the key, along with timestamps.
    - I was able to get the public certificate from firebase docs but wasn't able to generate a key to decode the custom-token, hence I have manually used a work around in those methods for now.
    - Can be solved if given more time and research.

2) Tried to generate the full_name key in a serializer for `accounts/profile/view/` but was unable to do so because of time constraints and old docs (used deprecated api which of course doesnt' work for our purpose)
