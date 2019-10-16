from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer
from .permissions import IsStaffOrReadOnly


class QuestionList(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly,]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
