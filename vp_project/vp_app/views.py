from django.utils import timezone
from rest_framework import (
    generics,
    authentication,
    permissions,
    views,
    status
)
from rest_framework.response import Response
from .models import Question, Answer, Reply
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    ReplySerializer,
    ResultsSerializer,
    RecordSerializer
)
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly


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


class QuestionAnswers(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
    ]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        """
        Display all possible answers to a question with id
        'question_id'.
        """
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question=question_id)


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
    ]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class ReplyList(generics.ListAPIView):
    # TODO: Make this a staff-only view, or delete if nothing uses it.
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class QuestionReplies(generics.ListCreateAPIView):
    # TODO: Make this view a "CreateAPIView" with permission "IsAuthenticated". No one needs to view individual replies.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = ReplySerializer

    def get_queryset(self):
        """
        Display all responses to a question with id 'question_id'.
        """
        question_id = self.kwargs['question_id']
        return Reply.objects.filter(question=question_id)

    def perform_create(self, serializer):
        """
        Relate Users and Questions to Replies.
        """
        serializer.save(
            user=self.request.user,
            question=Question.objects.get(id=self.kwargs['question_id'])
        )

    def get(self, request, *args, **kwargs):
        """
        If the current date/time is after the Question was published,
        perform 'get()' as normal. Otherwise, return a 404. Staff users
        are always permitted.
        """
        question = Question.objects.get(id=self.kwargs['question_id'])
        if question.date_published <= timezone.now() \
                or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly, ]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class QuestionResults(generics.RetrieveAPIView):
    serializer_class = ResultsSerializer
    queryset = Question.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        If the current date/time is after the Question was concluded,
        perform 'retrieve()' as normal. Otherwise, return a 404. Staff
        users are always permitted.
        """
        print(self.kwargs)
        question = Question.objects.get(id=self.kwargs['pk'])
        if question.date_concluded <= timezone.now() \
                or request.user.is_staff:
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserRecord(views.APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = RecordSerializer(user)
        return Response(serializer.data)


