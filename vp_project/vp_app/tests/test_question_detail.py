from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


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
        response = self.client.get(
            reverse('question-detail', args=[2])
        )
        self.assertEqual(response.status_code, 404)

    def test_get_question(self):
        """
        Users can access a Question.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
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
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
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
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_nonstaff_update_question(self):
        """
        Non-staff users cannot update a Question.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        data = {'content': 'question 2'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_nonstaff_delete_question(self):
        """
        Non-staff users cannot delete a Question.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_update_question(self):
        """
        Anonymous users cannot update a Question.
        """
        data = {'content': 'question 2'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_delete_question(self):
        """
        Anonymous users cannot delete a Question.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)
