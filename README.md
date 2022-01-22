# froidapi (Farsroid API)

## Introduction 🗣️

Froid API (Farsroid API) is an unofficial micro RESTful API for [Farsroid](https://www.farsroid.com  'Farsroid Homepage').

It is written in [Python](https://www.python.org  'Python Homepage') and uses

[FastAPI](https://fastapi.tiangolo.com/  'FastAPI Documentation') web framework. Froid API can be easily extended

or modified to suit your needs. You can deploy it right away on

your own server or on a PaaS service like [Heroku](https://www.heroku.com) or [Railway](https://railway.app/).

## Features ⚒️

- **RESTful API** with readable **JSON** responses.

- User **Authentication** with an API key (`X-API-KEY` header) to access restricted resources.

- **CORS** (Cross-Origin Resource Sharing) enabled for all endpoints. This is required for the frontend to work.

- Full **SwaggerUI** documentation available at `/v1/docs` endpoint.

- ORM database integration with [SQLAlchemy](https://www.sqlalchemy.org/).

- Exclusive asynchronous API handlers for [Farsroid](https://www.farsroid.com) to make it easier to integrate with your existing application.

Exclusive API features:

- Fast and easy search for applications on [Farsroid](https://www.farsroid.com) using Farsroid's built-in `JSON` search API.

- Legacy search support that includes more detailed search results (`thumbnail`, `description`, etc.).

- Getting statistics (`downloads`, `views`, `ratings`) for applications.

- Getting comments (`comments`) for a specific application.

- Getting download page for a specific application (this includes download links, related applications, etc.).

- More to come...

## Development 🚧 and Deployment 🚀

If you want to contribute to the project, the best way is to fork the repository and make your own changes to the code
and create a pull request.

A few steps to get started:

1. Clone the repository: `git clone https://github.com/IHosseini083/froidapi.git`

2. Install the dependencies: `pip install -r requirements.txt`

3. Make your changes and then `git add . && git commit -m "Your commit message"`

4. Create a pull request

5. Wait for the approval

How to start development server:

1. First, you need to install the dependencies you have not yet: `pip install -r requirements.txt`

2. Run `python -m uvicorn main:app --reload` in the project root directory

3. Open `http://localhost:8000/v1/docs` in your browser to see the documentation 🙂

You can also use the below code to run the development server just by running the `main.py` file:

```python
import uvicorn
from fastapi import FastAPI  

app = FastAPI()

# other path operations and settings
...

if  __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

There several options for you to deploy this app on a remote server, but here is two services you can use for free:

The first one and the famous one is [Heroku](https://heroku.com), Heroku provides you a free plan to deploy your web applications as quick as possible. By default, this repository is configured to be deployed on Heroku, all you need to do is to fork this repository, register your account for Heroku from [here](https://signup.heroku.com/login), download the Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install), and run the bellow commands step by step.

At first, you need to login from the CLI:

```bash
>> heroku login
```

This will open a web browser and prompts you to login with your account.

After that you logged in via the CLI, you run the bellow command to create a new app on Heroku (if you don't want to create it manually from Heroku dashboard)

```bash
>> heroku create [<YOUR_APP_NAME>]
```

It will create an application for you with the given name (if the names is valid and is not already taken by another user).

Then you have to connect to the remote git that Heroku holds for your app:

```bash
>> heroku git:remote -a [<YOUR_APP_NAME>]
```

And then you can push the repository to Heroku:

```bash
>> git push heroku master
```

Now heroku will deploy your app to the Heroku servers and install the dependencies for you automatically.
You can access your app from `http://<YOUR_APP_NAME>.herokuapp.com`

Notes:

- After making changes to your code, you need to run `git add . && git commit -m "Your commit message"` 
and then `git push heroku master` to deploy your changes to Heroku.
- You can also use `heroku logs` to see the logs of your app on your terminal.
- Every new library that you install must be included in `requirements.txt` file so that Heroku will install it.
- By, default, we are using `gunicorn` as a master process and `uvicorn` as worker processes.

## Usage

## Documentation

## Credits

## License
