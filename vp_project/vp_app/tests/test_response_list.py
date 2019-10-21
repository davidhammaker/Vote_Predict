from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Response


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class ResponseListTests(APITestCase):
    url = reverse('response-list')

    def setUp(self) -> None:
        question = Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )
        Answer.objects.create(
            content='answer 1',
            question=question
        )
        Answer.objects.create(
            content='answer 2',
            question=question
        )
        User.objects.create_user(username='test_user_1')
        User.objects.create_user(username='test_user_2')

    def test_no_responses(self):
        """
        If no Responses have been created, the API should return an
        empty list.
        """
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [])

    def test_get_responses(self):
        """
        If any Responses exist, the API should list them.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        Response.objects.create(
            user=user_1,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        Response.objects.create(
            user=user_2,
            question=question,
            vote=answer_2,
            prediction=answer_1
        )
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [
            {
                'id': 1,
                'user': 1,
                'question': 1,
                'vote': 1,
                'prediction': 2
            },
            {
                'id': 2,
                'user': 2,
                'question': 1,
                'vote': 2,
                'prediction': 1
            }
        ])
