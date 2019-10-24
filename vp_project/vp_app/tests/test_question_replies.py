from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Reply


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class QuestionRepliesTests(APITestCase):
    url = reverse('question-replies', args=[1])

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

    def test_no_replies(self):
        """
        If no Replies have been created, the API should return an
        empty list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_replies(self):
        """
        If any Replies exist for the, the API should list them (and no
        others).
        """
        question_1 = Question.objects.get(id=1)
        question_2 = Question.objects.get(id=2)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        answer_3 = Answer.objects.get(id=3)
        answer_4 = Answer.objects.get(id=4)
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        Reply.objects.create(
            user=user_1,
            question=question_1,
            vote=answer_1,
            prediction=answer_2
        )
        Reply.objects.create(
            user=user_2,
            question=question_1,
            vote=answer_2,
            prediction=answer_1
        )
        # Reply that should not show up:
        Reply.objects.create(
            user=user_1,
            question=question_2,
            vote=answer_3,
            prediction=answer_4
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
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

    def test_new_reply(self):
        """
        Users can create new Replies.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        data = {'vote': 1, 'prediction': 2}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 1,
            'prediction': 2
        })

    def test_anonymous_reply(self):
        """
        Anonymous users cannot create new Replies.
        """
        data = {'vote': 1, 'prediction': 2}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)

    def test_multiple_replies(self):
        """
        Users cannot send more than one Reply per Question.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        data = {'vote': 1, 'prediction': 2}
        response_1 = self.client.post(self.url, data)
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_1.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 1,
            'prediction': 2
        })
        data = {'vote': 1, 'prediction': 1}
        response_2 = self.client.post(self.url, data)
        self.assertEqual(response_2.status_code, 400)

    def test_multiple_users_replies(self):
        """
        Multiple Users may create Replies to a single Question
        """
        user_1 = User.objects.get(id=1)
        self.client.force_authenticate(user=user_1)
        data = {'vote': 1, 'prediction': 2}
        response_1 = self.client.post(self.url, data)
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_1.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 1,
            'prediction': 2
        })
        self.client.logout()
        user_2 = User.objects.get(id=2)
        self.client.force_authenticate(user=user_2)
        data = {'vote': 2, 'prediction': 1}
        response_2 = self.client.post(self.url, data)
        self.assertEqual(response_2.status_code, 201)
        self.assertEqual(response_2.data, {
            'id': 2,
            'user': 2,
            'question': 1,
            'vote': 2,
            'prediction': 1
        })

    def test_invalid_vote(self):
        """
        User votes must correspond to an Answer to the Question.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        data = {'vote': 3, 'prediction': 2}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid vote.', str(response.data))

    def test_invalid_prediction(self):
        """
        User predictions must correspond to an Answer to the Question.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        data = {'vote': 1, 'prediction': 3}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid prediction.', str(response.data))
