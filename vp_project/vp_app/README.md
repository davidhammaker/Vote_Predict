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
    * There is currently only one serializer in this file: **QuestionSerializer**. The serializer inherits from the [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer), and therefore has built-in functionality for creating, listing, and updating. The provided fields configure specifically what elements of the _Question_ model the serializer will convert.

#### `views.py`
* Represent the converted data from the serializer.
    * There is currently only one view configured: **QuestionList**.
        * This view represents the full list of _Question_ model instances, which are serialized via the _QuestionSerializer_.
        * The view inherits from the [ListCreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview), and therefore supports listing and creating _Question_ model instances.

#### `urls.py`
* Configure URLs for the app.
    * There is currently only one URL configured for this app: `'questions-list'` at `questions/`.
        * This is the URL at which serialized data from the _QuestionList_ view may be found.
