from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from .models import Question, Answer


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class QuestionListTests(APITestCase):
    url = reverse('question-list')

    def test_no_questions(self):
        """
        If no Questions have been created, the API should return an
        empty list.
        """
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [])

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
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [
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
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [
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
        request = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(request.status_code, 201)

    def test_nonstaff_create_question(self):
        """
        Non-staff users may not create new Questions.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        request = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(request.status_code, 403)

    def test_anonymous_create_question(self):
        """
        Anonymous users may not create new Questions.
        """
        request = self.client.post(self.url, {
            'content': 'question 1',
            'date_published': '2019-10-19T04:25:00Z',
            'date_concluded': '2019-10-20T04:25:00Z',
        })
        self.assertEqual(request.status_code, 401)


class QuestionDetailTests(APITestCase):
    url = reverse('question-detail', args=[1])

    def setUp(self) -> None:
        Question.objects.create(
                content='question 1',
                date_published=date,
                date_concluded=(date + timedelta(days=1))
        )

    def test_no_question(self):
        """
        Users cannot access a non-existent Question.
        """
        request = self.client.get(
            reverse('question-detail', args=[2])
        )
        self.assertEqual(request.status_code, 404)

    def test_get_question(self):
        """
        Users can access a Question.
        """
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
                'id': 1,
                'content': 'question 1',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': []
        })

    def test_update_question(self):
        """
        Staff users can update a Question.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        data = {'content': 'question 2'}
        request = self.client.put(self.url, data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
                'id': 1,
                'content': 'question 2',
                'date_published': '2019-10-19T04:25:00Z',
                'date_concluded': '2019-10-20T04:25:00Z',
                'answers': []
        })

    def test_delete_question(self):
        """
        Staff users can delete a Question.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 204)

    def test_nonstaff_update_question(self):
        """
        Non-staff users cannot update a Question.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        data = {'content': 'question 2'}
        request = self.client.put(self.url, data)
        self.assertEqual(request.status_code, 403)

    def test_nonstaff_delete_question(self):
        """
        Non-staff users cannot delete a Question.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 403)

    def test_anonymous_update_question(self):
        """
        Anonymous users cannot update a Question.
        """
        data = {'content': 'question 2'}
        request = self.client.put(self.url, data)
        self.assertEqual(request.status_code, 403)

    def test_anonymous_delete_question(self):
        """
        Anonymous users cannot delete a Question.
        """
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 403)


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
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [])

    def test_answers(self):
        """
        The API should return all Answers to a question.
        """
        question = Question.objects.get(id=1)
        Answer.objects.create(content='answer 1', question=question)
        Answer.objects.create(content='answer 2', question=question)
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, [
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
        request = self.client.get('question-answers', args=[2])
        self.assertEqual(request.status_code, 404)

    def test_create_answer(self):
        """
        Staff users can create new Answers.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        request = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1,
        })
        self.assertEqual(request.status_code, 201)

    def test_nonstaff_create_answer(self):
        """
        Non-staff users cannot create new Answers.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        request = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1
        })
        self.assertEqual(request.status_code, 403)

    def test_anonymous_create_answer(self):
        """
        Anonymous users cannot create new Answers.
        """
        request = self.client.post(self.url, {
            'content': 'answer 1',
            'question': 1
        })
        self.assertEqual(request.status_code, 401)
