from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Reply


date = timezone.now() - timedelta(days=1)


class ReplyDetailTests(APITestCase):
    url = reverse('reply-detail', args=[1, 1])
    url_question_concluded = reverse('reply-detail', args=[2, 1])

    def setUp(self) -> None:
        question_1 = Question.objects.create(
            content='question 1',
            date_published=date,
            date_concluded=(date + timedelta(days=2))
        )
        Answer.objects.create(
            content='answer 1',
            question=question_1
        )
        Answer.objects.create(
            content='answer 2',
            question=question_1
        )

        # Concluded Question
        question_2 = Question.objects.create(
            content='question 2',
            date_published=(date - timedelta(days=1)),
            date_concluded=date
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

    def test_retrieve_reply(self):
        """
        Users can get Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 1,
            'prediction': 2
        })

    def test_update_reply(self):
        """
        Users can update Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 2}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'user': 1,
            'question': 1,
            'vote': 2,
            'prediction': 2
        })

    def test_update_reply_invalid_vote(self):
        """
        Users cannot update Replies with an invalid vote.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 3}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid vote.', str(response.data))

    def test_update_reply_invalid_prediction(self):
        """
        Users cannot update Replies with an invalid prediction.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'prediction': 3}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid prediction.', str(response.data))


    def test_delete_reply(self):
        """
        Users can delete Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_nonowner_update_reply(self):
        """
        Users cannot update Replies of other Users.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user_1 = User.objects.get(id=1)
        Reply.objects.create(
            user=user_1,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        user_2 = User.objects.get(id=2)
        self.client.force_authenticate(user=user_2)
        data = {'vote': 2}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_nonowner_delete_reply(self):
        """
        Users cannot delete Replies of other Users.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user_1 = User.objects.get(id=1)
        Reply.objects.create(
            user=user_1,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        user_2 = User.objects.get(id=2)
        self.client.force_authenticate(user=user_2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_update_reply(self):
        """
        Anonymous Users cannot update Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 2}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 401)

    def test_anonymous_delete_reply(self):
        """
        Anonymous Users cannot delete Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)

    def test_update_reply_concluded_question(self):
        """
        Users cannot update Replies to concluded questions.
        """
        question = Question.objects.get(id=2)
        answer_1 = Answer.objects.get(id=3)
        answer_2 = Answer.objects.get(id=4)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 3}
        response = self.client.patch(
            self.url_question_concluded,
            data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('question has concluded', str(response.data))
        data_2 = {'vote': 3, 'prediction': 4}
        response_2 = self.client.put(
            self.url_question_concluded,
            data_2
        )
        self.assertEqual(response_2.status_code, 400)
        self.assertIn('question has concluded', str(response_2.data))
