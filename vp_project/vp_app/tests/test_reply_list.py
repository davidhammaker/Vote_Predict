from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Reply


date = timezone.now() - timedelta(days=1)


class ReplyListTests(APITestCase):
    url = reverse('reply-list')

    def setUp(self) -> None:
        question_1 = Question.objects.create(
            content='question 1',
            date_published=(date - timedelta(days=1)),
            date_concluded=(date + timedelta(days=2))
        )
        answer_1 = Answer.objects.create(
            content='answer 1',
            question=question_1
        )
        answer_2 = Answer.objects.create(
            content='answer 2',
            question=question_1
        )

        question_2 = Question.objects.create(
            content='question 2',
            date_published=(date - timedelta(days=1)),
            date_concluded=(date + timedelta(days=2))
        )
        answer_3 = Answer.objects.create(
            content='answer 3',
            question=question_2
        )
        answer_4 = Answer.objects.create(
            content='answer 4',
            question=question_2
        )

        user_1 = User.objects.create_user(username='test_user_1')
        user_2 = User.objects.create_user(username='test_user_2')

        Reply.objects.create(
            question=question_1,
            user=user_1,
            vote=answer_1,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question_2,
            user=user_1,
            vote=answer_3,
            prediction=answer_4
        )
        Reply.objects.create(
            question=question_1,
            user=user_2,
            vote=answer_1,
            prediction=answer_2
        )

    def test_get_replies(self):
        """
        Users can get their own Replies.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'user': 1,
                'question': 1,
                'vote': 1,
                'prediction': 1
            },
            {
                'id': 2,
                'user': 1,
                'question': 2,
                'vote': 3,
                'prediction': 4
            },
        ])

    def test_no_replies(self):
        """
        Users view empty list if no replies exist.
        """
        user = User.objects.create(username='test_user_3')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_anonymous_replies(self):
        """
        Anonymous Users cannot view replies.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
