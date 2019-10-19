from rest_framework import generics, authentication, permissions
from .models import Question, Answer, Response
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    ResponseSerializer,
)
from .permissions import IsStaffOrReadOnly


class QuestionList(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionAnswers(generics.ListAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        """
        Display all possible answers to a question with id
        'question_id'.
        """
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question=question_id)


class AnswerList(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class ResponseList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = ResponseSerializer
    queryset = Response.objects.all()

    def perform_create(self, serializer):
        """
        Relate users to responses.
        """
        serializer.save(user=self.request.user)


class QuestionResponses(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = ResponseSerializer

    def get_queryset(self):
        """
        Display all responses to a question with id 'question_id'.
        """
        question_id = self.kwargs['question_id']
        return Response.objects.filter(question=question_id)

    def perform_create(self, serializer):
        """
        Relate Users and Questions to Responses.
        """
        serializer.save(
            user=self.request.user,
            question=Question.objects.get(id=self.kwargs['question_id'])
        )
