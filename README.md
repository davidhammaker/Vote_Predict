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
