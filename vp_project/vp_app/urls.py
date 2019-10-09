from django.urls import path
from . import views as vp_app_views

urlpatterns = [
    path(
        'questions/',
        vp_app_views.QuestionList.as_view(),
        name='question-list'
    ),
]
