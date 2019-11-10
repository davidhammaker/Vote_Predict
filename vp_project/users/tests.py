from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Profile


class UserCreateTests(APITestCase):
    url = reverse('create-user')

    def test_create_user(self):
        """
        A new User can be created.
        """
        data = {
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['username'],
            'testusername'
        )
        self.assertEqual(
            response.data['email'],
            'testemail@example.com'
        )
        self.assertEqual(len(response.data), 3)

    def test_create_user_no_username(self):
        """
        A User cannot be created without a username.
        """
        data = {
            'email': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['username'][0],
            'This field is required.'
        )

    def test_create_user_no_email(self):
        """
        A User cannot be created without an email address.
        """
        data = {
            'username': 'testusername',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['email'][0],
            'This field is required.'
        )

    def test_create_user_no_password(self):
        """
        A User cannot be created without a password.
        """
        data = {
            'username': 'testusername',
            'email': 'testemail@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['password'][0],
            'This field is required.'
        )

    def test_create_user_duplicate_username(self):
        """
        A User cannot be created with a duplicate username.
        """
        User.objects.create_user(
            username='testusername',
            email='new@example.com',
            password='testpassword123'
        )
        data = {
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['username'][0],
            'A user with that username already exists.'
        )

    def test_create_user_duplicate_email(self):
        """
        A User cannot be created with a duplicate email address.
        """
        User.objects.create_user(
            username='newusername',
            email='testemail@example.com',
            password='testpassword123'
        )
        data = {
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['email'][0],
            'This field must be unique.'
        )

    def test_profile_creation(self):
        """
        A Profile is created whenever a User is created.
        """
        data = {
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        profile = Profile.objects.get(user=response.data['id'])
        user = User.objects.get(id=response.data['id'])
        self.assertEqual(profile.user, user)


class ProfileDetailTests(APITestCase):
    url = reverse('profile')

    def setUp(self) -> None:
        user = User.objects.create_user(
            username='testusername',
            email='new@example.com',
            password='testpassword123'
        )
        Profile.objects.create(
            user=user
        )

    def test_get_profile(self):
        """
        An authenticated User can access a corresponding Profile.
        """
        user = User.objects.first()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], 1)

    def test_update_profile(self):
        """
        An authenticated User can update a corresponding Profile.
        """
        user = User.objects.first()
        self.client.force_authenticate(user=user)
        data = {'location': 'florida'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['location'], 'florida')

    def test_anonymous_get_profile(self):
        """
        Unauthenticated User cannot access a Profile.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_anonymous_update_profile(self):
        """
        Unauthenticated User cannot update a Profile.
        """
        data = {'location': 'florida'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, 401)
