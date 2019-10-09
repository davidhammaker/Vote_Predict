# Vote Predict

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
1. Create the environment variable "Secret" (preferred). There is an excellent tutorial for doing this on [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8) or [Mac/Linux](https://www.youtube.com/watch?v=5iWhQWVXosU). If you are using Git Bash for Windows, the Mac/Linux tutorial may be more helpful. The string you use for "Secret" can be anything, typically long and full of random characters. Remember to restart all terminals after modifying your environment variables.
2. Open "vp_project/vp_project/settings.py" and replace `SECRET_KEY = os.environ.get("SECRET")` with `SECRET_KEY = "some_string"`. This is by far the easier method, but it is much less secure, especially if you're sharing your code with others.

If you would like to access the project's [Django Admin Site](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/), you'll need to create a superuser:
```shell
$ django-admin createsuperuser
```

### Running Locally

Once you've set up the project, you can run the project locally:

```shell
$ cd vp_project
$ python manage.py runserver
```

If you go to http://localhost:8000/, you should be able to see the site up and running!
* This project is still in very early development, and the default Django DEBUG page is displayed at the site index. However, if you created a superuser, you can log into http://localhost:8000/admin/ to access the admin site.
