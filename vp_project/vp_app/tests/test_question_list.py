from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class QuestionListTests(APITestCase):
    url = reverse('question-list')

    def test_no_questions(self):
        """
        If no Questions have been created, the API should return an
        empty list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_questions(self):
        """
        If any Questions exist, the API should list them.
        """
        Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )
        Question.objects.create(
            content='question 2',
            date_published=date,
            date_concluded=(date + timedelta(days=1))
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'content': 'question 1',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': []
            },
            {
                'id': 2,
                'content': 'question 2',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': []
            },
        ])

    def test_get_questions_with_answers(self):
        """
        If any Questions exist with answers, the API should list
        them.
        """
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'content': 'question 1',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': [
                    1,
                    2
                ]
            },
            {
                'id': 2,
                'content': 'question 2',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': [
                    3,
                    4
                ]
            },
        ])

    def test_staff_create_question(self):
        """
        Staff users may create new Questions.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(response.status_code, 201)

    def test_nonstaff_create_question(self):
        """
        Non-staff users may not create new Questions.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(response.status_code, 403)

    def test_anonymous_create_question(self):
        """
        Anonymous users may not create new Questions.
        """
        response = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(response.status_code, 401)
