from datetime import timedelta, datetime
from django.urls import reverse
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class AnswerListTests(APITestCase):
    url = reverse('answer-list')

    def setUp(self) -> None:
        Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )

    def test_no_answers(self):
        """
        If no Answers have been created, the API should return an empty
        list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_questions(self):
        """
        If any Answers exist, the API should list them.
        """
        question = Question.objects.get(id=1)
        Answer.objects.create(
            content='answer 1',
            question=question
        )
        Answer.objects.create(
            content='answer 2',
            question=question
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'content': 'answer 1',
                'question': 1
            },
            {
                'id': 2,
                'content': 'answer 2',
                'question': 1
            },
        ])
