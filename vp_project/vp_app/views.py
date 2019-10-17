from rest_framework import generics
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .permissions import IsStaffOrReadOnly


class QuestionList(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
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
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly, ]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
