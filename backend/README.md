# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

#### For Unix based machine (Bash)
```bash
pip install -r requirements.txt
```
#### For Windows (Powershell)
```Powershell
pip install -r .\requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

---
### Set up the Database

- Make sure that Postgres is running and your current shell user has administrative access (can create database and users) to it.
- With Postgres running, and your shell user with administrative access, create a `trivia` database by running the `setup.sql` in the repo:

#### For all types of shell
```shell
psql -f setup.sql
```

- Populate the main database using the `trivia.psql` file in the repo. From the `backend` folder in terminal run:

#### For Unix based machine (Bash)
```bash
psql trivia < trivia.psql
```
#### For Windows (Powershell)
```Powershell
pip psql -f trivia.psql trivia
```

- You can also populate the test database using the `trivia.psql` file in the repo. From the `backend` folder in terminal run:

#### For Unix based machine (Bash)
```bash
psql trivia_test < trivia.psql
```
#### For Windows (Powershell)
```Powershell
pip psql -f trivia.psql trivia_test
```
- Setup the database connection information in the `.env` file inside the `backend` directory:

```
# settings
TRIVIA_DB=
TRIVIA_DB_USR=
TRIVIA_DB_USR_PWD=
TRIVIA_DB_HOST_PORT=
```
> Below the description of each environment variable:
> `TRIVIA_DB`: the database name of the Trivia app
> 
> `TRIVIA_DB_USR`: the username for `TRIVIA_DB`
> 
> `TRIVIA_DB_USR_PWD`: the password for `TRIVIA_DB_USR`
> 
> `TRIVIA_DB_HOST_PORT`= the host and port used to connect to `TRIVIA_DB`. The expected format for this variable is `HOST:PORT`
---
### Run the Server

- From within the `./backend` directory, first ensure you are working using your created virtual environment.
- Setup the following environment variables:
#### For Unix based machine (Bash)
```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=True
```
#### For Windows (Powershell)
```Powershell
$env:FLASK_APP="flaskr"
$env:FLASK_DEBUG="True"
```

To run the server, execute:

#### For all types of shell
```shell
flask run
```

The `FLASK_DEBUG` variable set to `True` will detect file changes and restart the server automatically.

---
## API documentation
---
### Requests based on categories
   
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
---
### Requests based on questions
1. Get all questions
   
`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` with type `integer`
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category blank string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": ""
}
```
---
1. Get questions per category

`GET '/categories/${id}/questions'`

- Fetches questions for a category specified by `id` request argument
- Request Arguments: `id` with type `integer`
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Science"
}
```

3. Search for specific questions

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category blank string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": ""
}
```

4. Create a new question

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

5. Delete a question

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` with type `integer`
- Returns: Does not need to return anything besides the appropriate HTTP status code.
---

### Requests based on quizzes
`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": ""
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```
---

## Testing

To deploy the tests, in the shell, make sure you are in the `backend` directory then run:

#### For Unix based machine (Bash)
```bash
psql -f setup.sql
psql trivia_test < trivia.psql
python test_flaskr.py
```
#### For Windows (Powershell)
```Powershell
psql -f setup.sql
psql -f trivia.psql trivia_test
python .\test_flaskr.py
```
