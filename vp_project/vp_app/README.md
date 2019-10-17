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
    * There is also an _AnswerSerializer_ with similar functionality.

#### `views.py`
* Represent the converted data from the serializer.
    * Example view: **QuestionList**.
        * This view represents the full list of _Question_ model instances, which are serialized via the _QuestionSerializer_.
        * The view inherits from the [ListCreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview), and therefore supports listing and creating _Question_ model instances.
        * Note that _QuestionList_ has one listed permission class: "_IsStaffOrReadOnly_". If you access this view (see [`urls.py`](https://github.com/davidhammaker/Vote_Predict_Backend/tree/master/vp_project/vp_app#urlspy) below), the API will display a form field if you are logged in as a staff user, such as a superuser.
    * There are several other views to provide access to _Question_ and _Answer_ instances. See `urls.py` to access them via the API.

#### `permissions.py`
* Defines all custom permissions used in this app.
    * There is currently only one custom permission class: **IsStaffOrReadOnly**.
        * Staff users (including superusers) will have full rights to any views with this permission class. Other users will only be able to use "Safe" HTTP requests like GET and OPTIONS. For example, this class is used in the _QuestionsList_ view so that only site staff will be able to create new questions.

#### `urls.py`
* Configure URLs for the app.
    * Example URL: `'questions-list'` at `questions/`.
        * This is the URL at which serialized data from the _QuestionList_ view may be found.
    * There are several other URLs listed in the file, each of which points to a different view of the API.
