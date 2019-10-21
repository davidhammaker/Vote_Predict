from datetime import timedelta, datetime
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer


date = datetime(2019, 10, 19, 4, 25, tzinfo=pytz.utc)


class AnswerListTests(APITestCase):
    url = reverse('answer-detail', args=[1])

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

    def test_no_answer(self):
        """
        Users cannot access a non-existent Answer.
        """
        request = self.client.get(reverse('answer-detail', args=[2]))
        self.assertEqual(request.status_code, 404)

    def test_get_answer(self):
        """
        Users can access an Answer.
        """
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            'id': 1,
            'content': 'answer 1',
            'question': 1
        })

    def test_update_answer(self):
        """
        Staff users can update an Answer.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        data = {'content': 'answer 2'}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            'id': 1,
            'content': 'answer 2',
            'question': 1
        })

    def test_delete_answer(self):
        """
        Staff users can delete an Answer.
        """
        user = User.objects.create_user(username='test_user')
        user.is_staff = True
        self.client.force_authenticate(user=user)
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 204)

    def test_nonstaff_update_answer(self):
        """
        Non-staff users cannot update an Answer.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        data = {'content': 'answer 2'}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 403)

    def test_nonstaff_delete_answer(self):
        """
        Non-staff users cannot delete an Answer.
        """
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user=user)
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 403)

    def test_anonymous_update_answer(self):
        """
        Anonymous users cannot update an Answer.
        """
        data = {'content': 'answer 2'}
        request = self.client.patch(self.url, data)
        self.assertEqual(request.status_code, 401)

    def test_anonymous_delete_answer(self):
        """
        Anonymous users cannot delete an Answer.
        """
        request = self.client.delete(self.url)
        self.assertEqual(request.status_code, 401)

