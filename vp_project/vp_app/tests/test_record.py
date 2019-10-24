from datetime import timedelta, datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import pytz
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Response


date_today = timezone.now()
date_yesterday = date_today - timedelta(days=1)
date_two_days_ago = date_today - timedelta(days=2)
date_tomorrow = date_today + timedelta(days=1)


class RecordTests(APITestCase):
    url = reverse('record')

    def setUp(self) -> None:

        # Questions and Answers:
        question_1 = Question.objects.create(
            content='question 1',
            date_published=date_two_days_ago,
            date_concluded=date_yesterday
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
            date_published=date_two_days_ago,
            date_concluded=date_yesterday
        )
        answer_3 = Answer.objects.create(
            content='answer 3',
            question=question_2
        )
        answer_4 = Answer.objects.create(
            content='answer 4',
            question=question_2
        )

        question_3 = Question.objects.create(
            content='question 3',
            date_published=date_two_days_ago,
            date_concluded=date_yesterday
        )
        answer_5 = Answer.objects.create(
            content='answer 5',
            question=question_3
        )
        answer_6 = Answer.objects.create(
            content='answer 6',
            question=question_3
        )

        # Question concludes in the future and should not appear in
        # records:
        question_4 = Question.objects.create(
            content='question 4',
            date_published=date_yesterday,
            date_concluded=date_tomorrow
        )
        answer_7 = Answer.objects.create(
            content='answer 7',
            question=question_4
        )
        answer_8 = Answer.objects.create(
            content='answer 8',
            question=question_4
        )

        user_1 = User.objects.create_user(username='test_user_1')
        user_2 = User.objects.create_user(username='test_user_2')
        user_3 = User.objects.create_user(username='test_user_3')

        # User 1 Responses
        Response.objects.create(
            question=question_1,
            user=user_1,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question_2,
            user=user_1,
            vote=answer_3,
            prediction=answer_3
        )
        Response.objects.create(
            question=question_3,
            user=user_1,
            vote=answer_5,
            prediction=answer_5
        )
        Response.objects.create(
            question=question_4,
            user=user_1,
            vote=answer_7,
            prediction=answer_7
        )

        # User 2 Responses
        Response.objects.create(
            question=question_1,
            user=user_2,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question_2,
            user=user_2,
            vote=answer_3,
            prediction=answer_4
        )
        Response.objects.create(
            question=question_3,
            user=user_2,
            vote=answer_6,
            prediction=answer_5
        )
        Response.objects.create(
            question=question_4,
            user=user_2,
            vote=answer_7,
            prediction=answer_8
        )

        # User 3 Responses
        Response.objects.create(
            question=question_1,
            user=user_3,
            vote=answer_1,
            prediction=answer_1
        )
        Response.objects.create(
            question=question_2,
            user=user_3,
            vote=answer_3,
            prediction=answer_3
        )
        Response.objects.create(
            question=question_3,
            user=user_3,
            vote=answer_6,
            prediction=answer_5
        )
        Response.objects.create(
            question=question_4,
            user=user_3,
            vote=answer_7,
            prediction=answer_7
        )

    def test_get_record(self):
        """
        Users can retrieve their own records.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data, {
            "id": 1,
            "total_responses": 3,
            "correct_predictions": 2
        })

    def test_anonymous_get_record(self):
        """
        Anonymous users cannot retrieve records.
        """
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 403)
