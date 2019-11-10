from django.urls import path
from rest_framework.authtoken import views as authtoken_views
from . import views as users_views

urlpatterns = [
    path('api-token-auth/', authtoken_views.obtain_auth_token),
    path('users/', users_views.UserCreate.as_view(), name='create-user'),
    path(
        'profile/',
        users_views.ProfileDetail.as_view(),
        name='profile'
    ),
]
