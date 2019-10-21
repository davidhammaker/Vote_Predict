## vp_app
_Vote-Predict App_

### Quick Guide
#### `admin.py`
* Register the _Question_ model with the project's admin site.
    * Each _Question_ features content and date fields, plus inline _Answer_ fields.

#### `models.py`
* Create models to be used throughout the application.
    * The **Question** model has a "content" field to hold the actual text of the question, and "date_published" and "date_concluded" fields to represent the window of time in which the question will be active.
    * The **Answer** model has a "content" field to hold the actual text of the answer, and a foreign key relationship ("question") to connect the _Answer_ to its corresponding _Question_.
    * The **Response** model is composed entirely of foreign key relationships to represent a "user" response to a given "question", in which a user provides a "vote" and a "prediction", both of which are _Answer_ model instances.
    * The **Record** model is intended to be an extension of the built-in _User_ model, and it has fields to keep track of a user's "total_responses" and "correct_predictions".

#### `serializers.py`
* Create serializers to convert Python datatypes to and from API data like JSON.
    * Example serializer: **QuestionSerializer**. The serializer inherits from the [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer), and therefore has built-in functionality for creating, listing, and updating. The provided fields configure specifically what elements of the _Question_ model the serializer will convert.
    * There is also _AnswerSerializer_ with similar functionality to _QuestionSerializer_.
    * _ResponseSerializer_ has the same features as _QuestionSerializer_ and _AnswerSerializer_, but with a few additions. The `ReadOnlyField` specifies that users will be represented by their IDs, and the _Response_ user cannot be modified. The `validate` method checks the database for an existing _Response_ instance with the same _Question_ and _User_, then throws an error if one is found. The error ensures that users can only submit one response per question.

#### `views.py`
* Represent the converted data from the serializer.
    * Example view: **QuestionList**.
        * This view represents the full list of _Question_ model instances, which are serialized via the _QuestionSerializer_.
        * The view inherits from the [ListCreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview), and therefore supports listing and creating _Question_ model instances.
        * Note that _QuestionList_ has one listed permission class: "_IsStaffOrReadOnly_". If you access this view (see [`urls.py`](https://github.com/davidhammaker/Vote_Predict_Backend/tree/master/vp_project/vp_app#urlspy) below), the API will display a form field if you are logged in as a staff user, such as a superuser.
    * There are several other views to provide access to _Question_, _Answer_, and _Response_ instances. See `urls.py` to access them via the API.

#### `permissions.py`
* Defines all custom permissions used in this app.
    * There is currently only one custom permission class: **IsStaffOrReadOnly**.
        * Staff users (including superusers) will have full rights to any views with this permission class. Other users will only be able to use "Safe" HTTP requests like GET and OPTIONS. For example, this class is used in the _QuestionsList_ view so that only site staff will be able to create new questions.

#### `urls.py`
* Configure URLs for the app.
    * Example URL: `'questions-list'` at `questions/`.
        * This is the URL at which serialized data from the _QuestionList_ view may be found.
    * There are several other URLs listed in the file, each of which points to a different view of the API.

#### `tests/`
* Directory for all `vp_app` tests.
    * Each test file should follow the format `test_*.py`.
    * These tests exist to ensure that _everything_ is always working as expected. This repository is linked to [Travis CI](https://travis-ci.org/davidhammaker/Vote_Predict_Backend) and [CodeCov](https://codecov.io/gh/davidhammaker/Vote_Predict_Backend), which both demonstrate the current state of the application from a testing perspective. The code should be error-free at all times, if possible, and the scope of the tests should cover as much code as possible.
    * Click on any `test_*.py` file to see what tests are being run.
        * If you look at `test_question_list.py`, you'll find several tests, including `test_get_questions()`, which simply tests that the API returns the _Question_ instances that are available. The test begins by creating a few dummy _Question_ instances, then requests the view (`self.url`, which equals the URL for the `questions-list` view) via an HTTP _GET_ request. The test then asserts two things:
            1. The request's HTTP status code is `200 OK`, to verify that the API succeeded in responding to the GET request.
            2. The returned data from the API is equal to the data we expected, which is a list containing the two dictionaries representing the _Question_ instances we created.
        * All tests vary slightly from one another, but the above is a fairly simple example, and many tests in this repository will resemble it in some way, by checking status codes and returned data for expected results.
