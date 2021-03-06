# Froid API (Farsroid API)

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

- Getting statistics (`downloads`, `views`, `ratings`, etc.) for applications.

- Getting comments for a specific application.

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

There several options for you to deploy this app on a remote server, but here is a simple example:

One of the most popular options [Heroku](https://heroku.com), Heroku provides you a free plan to deploy your web applications as quick as possible. By default, this repository is configured to be deployed on Heroku, all you need to do is to fork this repository, register your account for Heroku from [here](https://signup.heroku.com/login), download the Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install), and run the bellow commands step by step.

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

⚠️ Important notes for Heroku users:

- After making changes to your code, you need to run `git add . && git commit -m "Your commit message"`
and then `git push heroku master` to deploy your changes to Heroku.
- You can also use `heroku logs` to see the logs of your app on your terminal.
- Every new library that you install must be included in `requirements.txt` file so that Heroku will install it.
- By default, we are using `gunicorn` as a master process and `uvicorn` as worker processes.
- Heroku provides a free `PostgreSQL` database for you to use in your app. You must install it manually from `Resources` section of your app dashboard.
If you are not using `PostgreSQL`, you can use any other database that Heroku provides in a paid plan.
This is because file-based databases are not supported by Heroku, and they will be removed at most in the next few hours.

Full documentation to deploy your app on Heroku using git can be found [here](https://devcenter.heroku.com/articles/git).
You can also deploy your app using [Github integration](https://devcenter.heroku.com/articles/github-integration) for Heroku.

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## How to use the API 🤔

Now you may be wondering how to use the API after you have deployed it to Heroku (or any other remote server) or run it locally.
If you go ahead and reach the `http://<YOUR_APP_NAME>.herokuapp.com/v1/docs` in your browser, you will see the documentation of the API.
There are two sections in the documentation:

- **Users**: This section contains the endpoints that you can use to create, update, delete and retrieve users and their information (e.g. email, token, etc.).
- **Posts**: This section contains the endpoints that you can use to actually interact with [Farsroid](https://www.farsroid.com) posts.

The **Posts** section requires you to have a valid token in the `X-API-Key` header of your requests.
How to get a valid token? Follow the steps below:

1. Create a new user with the `POST /v1/users/register` endpoint.
2. Now create a new token with the `POST /v1/users/me/token/new` endpoint (This generates a new random token for you in the database).

⚠️ See the API documentation for more details about the endpoints and their parameters.

How to use the generated token? Add the `X-API-Key` header to your requests with the token you generated:

```python
import requests
# headers to be sent with the request:
headers = {
    'X-API-Key': '<YOUR_TOKEN>'
}
# make a request to the endpoint:
query = "Spotify"
url = f"https://<YOUR_APP_NAME>.herokuapp.com/v1/posts/search?q={query}"
r = requests.get(url, headers=headers)
# print the response:
print(r.json())  # you can also use `r.text` to get the response as a string
```

If you want to test the API from the documentation page, you can pass your token to the `Authorize` section of the documentation page.

## Documentation 📖

To see the API documentation, you can go to `/v1/docs` endpoint in your browser.
It will open a `SwaggerUI` page that you can use to see the documentation of the API endpoints.
Documentation includes the description of each endpoint, the request parameters, the response status codes, and the response body.

## License ©️

This project is licensed under the GNU General Public License v3.0.
You can find the full license text in [here](LICENSE.txt).

[![License: GPL v3.0](https://img.shields.io/badge/License-GPL%20v3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contributing 💪

Anyone is welcome to contribute to this project by opening an issue or creating a pull request.
It is by contributing that you can improve the quality of the project and help others.

## TODOs 📝

Check [here](TODO.md) to see the list of things that have to be done or fixed.

## Screenshots 📸

![Docs page](https://github.com/IHosseini083/froidapi/blob/master/screenshots/froidapi_v1_ss1.png)
![Getting post's stats](https://github.com/IHosseini083/froidapi/blob/master/screenshots/froidapi_v1_ss2.png)
![Using legacy search](https://github.com/IHosseini083/froidapi/blob/master/screenshots/froidapi_v1_ss3.png)
