from django.db import models
from django.utils import timezone


class Question(models.Model):
    content = models.CharField(max_length=128)
    date_revealed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=64)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
