from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.CharField(max_length=128)
    date_published = models.DateTimeField(default=timezone.now)
    date_concluded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=64)
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content


class Reply(models.Model):
    user = models.ForeignKey(
        User,
        related_name='replies',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='replies',
        on_delete=models.CASCADE
    )
    vote = models.ForeignKey(
        Answer,
        related_name='votes',
        on_delete=models.CASCADE
    )
    prediction = models.ForeignKey(
        Answer,
        related_name='predictions',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.question.content

    class Meta:
        verbose_name_plural = "replies"

