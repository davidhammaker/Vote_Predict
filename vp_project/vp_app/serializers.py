from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Answer, Response


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'content',
            'date_published',
            'date_concluded',
            'answers'
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'content',
            'question'
        ]


class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        """
        Check that a user has not yet submitted a response for the given
        question. Users may only respond once per question.
        """
        existing_response = Response.objects.filter(
            user=self.context["request"].user.id,
            question=data['question']
        ).first()
        if existing_response:
            raise serializers.ValidationError(
                'Users may submit only one response per question.'
            )
        return data

    class Meta:
        model = Response
        fields = [
            'id',
            'user',
            'question',
            'vote',
            'prediction'
        ]