from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from users.models import Profile
from vp_app.models import Question, Answer, Reply


date = timezone.now() - timedelta(days=2)


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

        # Question 3 is in the future
        Question.objects.create(
            content='question 3',
            date_published=(date + timedelta(days=2)),
            date_concluded=(date + timedelta(days=3))
        )

        test_user_1 = User.objects.create_user(username='test_user_1')
        test_user_2 = User.objects.create_user(username='test_user_2')
        test_user_3 = User.objects.create_user(username='test_user_3')
        test_user_4 = User.objects.create_user(username='test_user_4')
        test_user_5 = User.objects.create_user(username='test_user_5')
        test_user_6 = User.objects.create_user(username='test_user_6')
        test_user_7 = User.objects.create_user(username='test_user_7')

        Profile.objects.create(user=test_user_1, location='florida')
        Profile.objects.create(user=test_user_2, location='florida')
        Profile.objects.create(user=test_user_3, location='florida')
        Profile.objects.create(user=test_user_4, location='florida')
        Profile.objects.create(user=test_user_5, location='colorado')
        Profile.objects.create(user=test_user_6, location='colorado')
        Profile.objects.create(user=test_user_7, location='colorado')

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
        Reply.objects.create(
            question=question,
            user=user_1,
            vote=answer_1,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question,
            user=user_2,
            vote=answer_1,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question,
            user=user_3,
            vote=answer_2,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question,
            user=user_4,
            vote=answer_2,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question,
            user=user_5,
            vote=answer_1,
            prediction=answer_1
        )
        Reply.objects.create(
            question=question,
            user=user_6,
            vote=answer_1,
            prediction=answer_2
        )
        Reply.objects.create(
            question=question,
            user=user_7,
            vote=answer_2,
            prediction=answer_2
        )
        # Dummy reply, which we expect to be excluded:
        Reply.objects.create(
            question=Question.objects.get(id=2),
            user=user_7,
            vote=Answer.objects.get(id=3),
            prediction=Answer.objects.get(id=4)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
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
            ],
            'location_results': [
                {
                    'vote': 1,
                    'location': 'florida',
                    'count': 2
                },
                {
                    'vote': 2,
                    'location': 'florida',
                    'count': 2
                },
                {
                    'vote': 1,
                    'location': 'colorado',
                    'count': 2
                },
                {
                    'vote': 2,
                    'location': 'colorado',
                    'count': 1
                }
            ]
        })

    def test_get_empty_results(self):
        """
        Users can retrieve results, even if there were no replies.
        """

        # Dummy reply, which we expect to be excluded:
        Reply.objects.create(
            question=Question.objects.get(id=2),
            user=User.objects.get(id=1),
            vote=Answer.objects.get(id=3),
            prediction=Answer.objects.get(id=4)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
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
            ],
            'location_results': []
        })

    def test_get_future_results(self):
        """
        Normal users cannot access results for a Question that has not
        yet concluded.
        """
        response = self.client.get(
            reverse('question-results', args=[3])
        )
        self.assertEqual(response.status_code, 404)

    def test_staff_get_future_results(self):
        """
        Staff users can access results for a Question that has not yet
        concluded.
        """
        user = User.objects.get(id=1)
        user.is_staff = True
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('question-results', args=[3])
        )
        self.assertEqual(response.status_code, 200)
