from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Response


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class ResponseDetailTests(APITestCase):
    url = reverse('response-detail', args=[1, 1])

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

    def test_update_response(self):
        """
        Users can update Responses.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 2}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 2,
            'prediction': 2
        })

    def test_update_response_invalid_vote(self):
        """
        Users cannot update Responses with an invalid vote.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 3}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 400)
        self.assertIn('Invalid vote.', str(request.data))

    def test_update_response_invalid_prediction(self):
        """
        Users cannot update Responses with an invalid prediction.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'prediction': 3}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 400)
        self.assertIn('Invalid prediction.', str(request.data))


    def test_delete_response(self):
        """
        Users can delete Responses.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 204)

    def test_nonowner_update_response(self):
        """
        Users cannot update Responses of other Users.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user_1 = User.objects.get(id=1)
        Response.objects.create(
            user=user_1,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        user_2 = User.objects.get(id=2)
        self.client.force_authenticate(user=user_2)
        data = {'vote': 2}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 403)

    def test_nonowner_delete_response(self):
        """
        Users cannot delete Responses of other Users.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user_1 = User.objects.get(id=1)
        Response.objects.create(
            user=user_1,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        user_2 = User.objects.get(id=2)
        self.client.force_authenticate(user=user_2)
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 403)

    def test_anonymous_update_response(self):
        """
        Anonymous Users cannot update Responses.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 2}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 401)

    def test_anonymous_delete_response(self):
        """
        Anonymous Users cannot delete Responses.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        Response.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 401)
