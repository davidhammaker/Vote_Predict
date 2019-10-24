from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class QuestionAnswersTests(APITestCase):
    url = reverse('question-answers', args=[1])

    def setUp(self) -> None:
        Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )

    def test_no_answers(self):
        """
        If there are no Answers, the API should return an empty list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_answers(self):
        """
        The API should return all Answers to a question.
        """
        question = Question.objects.get(id=1)
        Answer.objects.create(content='answer 1', question=question)
        Answer.objects.create(content='answer 2', question=question)
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
            }
        ])

    def test_answers_no_question(self):
        """
        If the Question does not exist, the API should return a 404.
        """
        response = self.client.get('question-answers', args=[2])
        self.assertEqual(response.status_code, 404)

    def test_create_answer(self):
        """
        Staff users can create new Answers.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1,
        })
        self.assertEqual(response.status_code, 201)

    def test_nonstaff_create_answer(self):
        """
        Non-staff users cannot create new Answers.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1
        })
        self.assertEqual(response.status_code, 403)

    def test_anonymous_create_answer(self):
        """
        Anonymous users cannot create new Answers.
        """
        response = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1
        })
        self.assertEqual(response.status_code, 401)
