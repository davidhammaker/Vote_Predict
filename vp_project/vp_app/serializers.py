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
    question = serializers.ReadOnlyField(source='question.id')

    def validate(self, data):
        """
        Check that a user has not yet submitted a response for the given
        question. Users may only respond once per question. Check that
        the provided vote and prediction pertain to the question.
        """
        question_id = self.context['request'] \
            .parser_context['kwargs']['question_id']
        answers = [
            answer for answer in
            Question.objects.get(id=question_id).answers.all()
        ]
        answer_ids = [answer.id for answer in answers]
        request_method = self.context['request'].stream.method

        # Verify that the user has not previously responded to this
        # question.
        existing_response = Response.objects.filter(
            user=self.context['request'].user.id,
            question=question_id
        ).first()
        if existing_response and request_method == 'POST':
            raise serializers.ValidationError(
                'Users may submit only one response per question.'
            )

        # Verify that the response contains a valid vote.
        if 'vote' in data.keys():
            if data['vote'].id not in answer_ids:
                raise serializers.ValidationError(
                    f'Invalid vote. Choose one of the following: {answers}.'
                )

        # Verify that the response contains a valid prediction.
        if 'prediction' in data.keys():
            if data['prediction'].id not in answer_ids:
                raise serializers.ValidationError(
                    f'Invalid prediction. Choose one of the following: '
                    f'{answers}.'
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