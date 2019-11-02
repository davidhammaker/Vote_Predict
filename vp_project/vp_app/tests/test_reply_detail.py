from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from vp_app.models import Question, Answer, Reply


date = timezone.now() - timedelta(days=1)


class ReplyDetailTests(APITestCase):
    url = reverse('question-reply', args=[1])
    url_concluded_question = reverse('question-reply', args=[3])
    url_unpublished_question = reverse('question-reply', args=[4])

    def setUp(self) -> None:
        question_1 = Question.objects.create(
            content='question 1',
            date_published=(date - timedelta(days=1)),
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
        question_2 = Question.objects.create(
            content='question 2',
            date_published=(date - timedelta(days=1)),
            date_concluded=(date + timedelta(days=2))
        )
        Answer.objects.create(
            content='answer 3',
            question=question_2
        )
        Answer.objects.create(
            content='answer 4',
            question=question_2
        )

        # Concluded Question
        question_3 = Question.objects.create(
            content='question 3',
            date_published=(date - timedelta(days=1)),
            date_concluded=date
        )
        Answer.objects.create(
            content='answer 5',
            question=question_3
        )
        Answer.objects.create(
            content='answer 6',
            question=question_3
        )

        # Unpublished Question
        question_4 = Question.objects.create(
            content='question 4',
            date_published=(date + timedelta(days=2)),
            date_concluded=(date + timedelta(days=3))
        )
        Answer.objects.create(
            content='answer 7',
            question=question_4
        )
        Answer.objects.create(
            content='answer 8',
            question=question_4
        )

        User.objects.create_user(username='test_user_1')
        User.objects.create_user(username='test_user_2')

    def test_create_reply(self):
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

    def test_no_reply(self):
        """
        If no Reply has been created, the API should return a 404.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_reply(self):
        """
        Users can get Replies.
        """
        question = Question.objects.get(id=1)
        answer_1 = Answer.objects.get(id=1)
        answer_2 = Answer.objects.get(id=2)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
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

    def test_patch_reply(self):
        """
        Users can update Reply with PATCH.
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

    def test_put_reply(self):
        """
        Users can update Reply with PUT.
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
        data = {'vote': 2, 'prediction': 2}
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
        question = Question.objects.get(id=3)
        answer_1 = Answer.objects.get(id=5)
        answer_2 = Answer.objects.get(id=6)
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        Reply.objects.create(
            user=user,
            question=question,
            vote=answer_1,
            prediction=answer_2
        )
        data = {'vote': 6}
        response = self.client.patch(
            self.url_concluded_question,
            data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('question has concluded', str(response.data))
        data_2 = {'vote': 6, 'prediction': 6}
        response_2 = self.client.put(
            self.url_concluded_question,
            data_2
        )
        self.assertEqual(response_2.status_code, 400)
        self.assertIn('question has concluded', str(response_2.data))

    def test_get_reply_unpublished_question(self):
        """
        Users cannot get Replies to an unpublished Question.
        """
        user = User.objects.get(id=1)
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url_unpublished_question)
        self.assertEqual(response.status_code, 404)
