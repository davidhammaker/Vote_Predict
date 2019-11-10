from rest_framework import generics, permissions, authentication
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
        Profile.objects.create(user=new_user)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """
        Get Profile based on User.
        """
        return Profile.objects.get(user=self.request.user)
