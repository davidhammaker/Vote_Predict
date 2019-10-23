from django.contrib.auth.models import User
from django.utils import timezone
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


class ResultsSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'results',
        ]

    def get_results(self, question):
        results = []
        answers = [answer for answer in question.answers.all()]
        for answer in answers:
            results.append({
                'answer': answer.id,
                'votes': Response.objects.filter(
                    vote=answer.id).count(),
                'predictions': Response.objects.filter(
                    prediction=answer.id).count()
            })
        return results


class RecordSerializer(serializers.ModelSerializer):
    total_responses = serializers.SerializerMethodField()
    correct_predictions = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = [
            'id',
            'total_responses',
            'correct_predictions'
        ]

    def get_total_responses(self, user):
        """
        Get the User's total number of Responses, excluding Responses to
        Questions that have not yet concluded.
        """
        total_responses = Response.objects.filter(
            user=user,

            # The keyword below basically means
            # "question.date_concluded <= timezone.now()", to ensure
            # that we only consider Questions that have not yet
            # concluded.
            question__date_concluded__lte=timezone.now()

        ).count()
        return total_responses

    def get_correct_predictions(self, user):
        """
        Get the User's total number of Responses containing predictions
        that match the Question's Answer receiving the most votes,
        excluding Responses to Questions that have not yet concluded.
        """
        correct_predictions = 0
        responses = Response.objects.filter(
            user=user,

            # The keyword below basically means
            # "question.date_concluded <= timezone.now()", to ensure
            # that we only consider Questions that have not yet
            # concluded.
            question__date_concluded__lte=timezone.now()

        ).all()
        for response in responses:
            question = response.question
            most_votes = 0
            top_answer = None
            for answer in question.answers.all():
                if answer.votes.count() > most_votes:
                    most_votes = answer.votes.count()
                    top_answer = answer
            if response.prediction == top_answer:
                correct_predictions += 1
        return correct_predictions
