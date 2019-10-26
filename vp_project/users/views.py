from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Hash password and create user.
        """
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


# TODO: Authentication and Permissions, Test
class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Get Profile based on User.
        """
        user = User.objects.get(id=self.kwargs['pk'])
        return Profile.objects.get(user=user)
