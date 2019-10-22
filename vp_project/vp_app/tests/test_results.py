from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Response


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class QuestionResultsTests(APITestCase):
    url = reverse('question-results', args=[1])

    def setUp(self) -> None:
        question_1 = Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )
        Answer.objects.create(
            content='answer 1',
            question=question_1
        )
        Answer.objects.create(
            content='answer 2',
            question=question_1
        )
        question_2 = Question.objects.create(
            content='question 2',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )
        Answer.objects.create(
            content='answer 3',
            question=question_2
        )
        Answer.objects.create(
            content='answer 4',
            question=question_2
        )
        User.objects.create_user(username='test_user_1')
        User.objects.create_user(username='test_user_2')
        User.objects.create_user(username='test_user_3')
        User.objects.create_user(username='test_user_4')
        User.objects.create_user(username='test_user_5')
        User.objects.create_user(username='test_user_6')
        User.objects.create_user(username='test_user_7')

    def test_get_results(self):
        """
        Users can retrieve results.
        """
        question = Question.objects.get(id=1)
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        user_3 = User.objects.get(id=3)
        user_4 = User.objects.get(id=4)
        user_5 = User.objects.get(id=5)
        user_6 = User.objects.get(id=6)
        user_7 = User.objects.get(id=7)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        Response.objects.create(
            question=question,
            user=user_1,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question,
            user=user_2,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question,
            user=user_3,
            vote=answer_2,
            prediction=answer_1
        )
        Response.objects.create(
            question=question,
            user=user_4,
            vote=answer_2,
            prediction=answer_1
        )
        Response.objects.create(
            question=question,
            user=user_5,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question,
            user=user_6,
            vote=answer_1,
            prediction=answer_2
        )
        Response.objects.create(
            question=question,
            user=user_7,
            vote=answer_2,
            prediction=answer_2
        )
        # Dummy response, which we expect to be excluded:
        Response.objects.create(
            question=Question.objects.get(id=2),
            user=user_7,
            vote=Answer.objects.get(id=3),
            prediction=Answer.objects.get(id=4)
        )
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            'id': 1,
            'results': [
                {
                    'answer': 1,
                    'votes': 4,
                    'predictions': 5
                },
                {
                    'answer': 2,
                    'votes': 3,
                    'predictions': 2
                }
            ]
        })

    def test_get_empty_results(self):
        """
        Users can retrieve results, even if there were no responses.
        """
        # Dummy response, which we expect to be excluded:
        Response.objects.create(
            question=Question.objects.get(id=2),
            user=User.objects.get(id=1),
            vote=Answer.objects.get(id=3),
            prediction=Answer.objects.get(id=4)
        )
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            'id': 1,
            'results': [
                {
                    'answer': 1,
                    'votes': 0,
                    'predictions': 0
                },
                {
                    'answer': 2,
                    'votes': 0,
                    'predictions': 0
                }
            ]
        })
