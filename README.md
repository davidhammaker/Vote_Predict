# Vote Predict

[![Build Status](https://travis-ci.org/davidhammaker/Vote_Predict_Backend.svg?branch=master)](https://travis-ci.org/davidhammaker/Vote_Predict_Backend) [![codecov](https://codecov.io/gh/davidhammaker/Vote_Predict_Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/davidhammaker/Vote_Predict_Backend)

A web-app in which you pick one of two answers to the given question, then try to guess what other users have picked.

## Getting Started

### Requirements

_Vote Predict_ requires [Python 3.6](https://www.python.org/) or higher.

### Set-up

First, [clone](https://help.github.com/en/articles/cloning-a-repository) this repository:

```shell
$ git clone https://github.com/davidhammaker/Vote_Predict_Backend.git
$ cd Vote_Predict_Backend
```

Install requirements.
* I recommend using a [virtual environment](https://docs.python.org/3/library/venv.html). For example ([Git Bash](https://git-scm.com/downloads) for Windows):
```shell
$ python -m venv venv
$ source venv/Scripts/activate
```
* To install requirements:
```shell
$ pip install -r requirements.txt
```

There is one environment variable that needs to be set up, called "Secret". If you try running the app without the environment variable set up, you will get an error. You have two options:
1. Create the environment variable "SECRET" (preferred). There is an excellent tutorial for doing this on [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8) or [Mac/Linux](https://www.youtube.com/watch?v=5iWhQWVXosU). If you are using Git Bash for Windows, the Mac/Linux tutorial may be more helpful. The string you use for "SECRET" can be anything, typically long and full of random characters. Remember to restart all terminals after modifying your environment variables.
2. Open "vp_project/vp_project/settings.py" and replace `SECRET_KEY = os.environ.get("SECRET")` with `SECRET_KEY = "some_string"`. This is by far the easier method, but it is much less secure, especially if you're sharing your code with others.

You'll need to migrate the database before you can create any Users, Questions, Answers, etc. From the `vp_project` directory (containing `manage.py`), perform the following:
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

If you would like to access the project's [Django Admin Site](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/), you'll need to create a superuser. Try either of the following:
```shell
$ django-admin createsuperuser
$ python manage.py createsuperuser
```

### Running Locally

Once you've set up the project, you can run the project locally:

```shell
$ cd vp_project
$ python manage.py runserver
```

The site up and running! Navigate to any of the URLs below to find out.
* If you created a superuser, you can log into http://localhost:8000/admin/ to access the admin site.

URLs to try out:
* http://localhost:8000/users/
* http://localhost:8000/questions/
* http://localhost:8000/api-token-auth/
    * `api-token-auth/` accepts POST requests to log in users.
    * Use an HTTP tool like [Postman](https://www.getpostman.com/) to get a user token by sending a valid username and password in the body of your POST request.

### Testing

Please note that **tests are still in the works**. However, several tests have already been written. Ultimately, tests should cover as much of the code as possible.

To test the application, navigate to the `vp_project` directory (containing `manage.py` and `pytest.ini`). From here, you can run `pytest` to test the code.
* Alternatively, you can run `python manage.py test path/to/tests/` in traditional Django fashion. This method is a bit clunky and is not really recommended.

### The Code

See the [README for 'vp_app'](https://github.com/davidhammaker/Vote_Predict_Backend/tree/master/vp_project/vp_app) for a brief explanation of the code so far.
