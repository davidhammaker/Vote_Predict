from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS
from .models import Question, Answer, Reply


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


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    question = serializers.ReadOnlyField(source='question.id')

    def validate(self, data):
        """
        Check that a user has not yet submitted a reply for the given
        question. Users may only respond once per question. Check that
        the provided vote and prediction pertain to the question.
        """

        # The 'QuestionReplies' view queryset contains all Replies for a
        # single question. This view will have 'question_id' passed in
        # the URL.
        if 'question_id' in \
                self.context['request'].parser_context['kwargs']:
            question_id = self.context['request'] \
                .parser_context['kwargs']['question_id']

        # The 'ReplyDetail' view will have a 'pk' passed in the URL, not
        # 'question_id'. We can use that 'pk' to get the associated
        # 'question_id'.
        else:
            reply_id = \
                self.context['request'].parser_context['kwargs']['pk']
            question_id = Reply.objects.get(id=reply_id).question.id

        # Use 'question_id' to find associated Question and Answers.
        question = Question.objects.get(id=question_id)
        answers = [answer for answer in question.answers.all()]
        answer_ids = [answer.id for answer in answers]
        request_method = self.context['request'].stream.method

        # Verify that the user has not previously responded to this
        # question.
        existing_reply = Reply.objects.filter(
            user=self.context['request'].user.id,
            question=question
        ).first()
        if existing_reply and request_method == 'POST':
            raise serializers.ValidationError(
                'Users may submit only one reply per question.'
            )

        # Verify that the reply contains a valid vote.
        if 'vote' in data.keys():
            if data['vote'].id not in answer_ids:
                raise serializers.ValidationError(
                    f'Invalid vote. Choose one of the following: {answers}.'
                )

        # Verify that the reply contains a valid prediction.
        if 'prediction' in data.keys():
            if data['prediction'].id not in answer_ids:
                raise serializers.ValidationError(
                    f'Invalid prediction. Choose one of the following: '
                    f'{answers}.'
                )

        # Verify that non-safe request methods are not allowed after
        # conclusion. This excludes DELETE, which has no validation.
        if request_method not in SAFE_METHODS:
            if timezone.now() >= question.date_concluded:
                raise serializers.ValidationError(
                    'This question has concluded, and replies may not '
                    'be created or modified.'
                )

        return data

    class Meta:
        model = Reply
        fields = [
            'id',
            'user',
            'question',
            'vote',
            'prediction'
        ]


class ResultsSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    location_results = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'results',
            'location_results',
        ]

    def get_results(self, question):
        results = []
        answers = [answer for answer in question.answers.all()]
        for answer in answers:
            results.append({
                'answer': answer.id,
                'votes': Reply.objects.filter(
                    vote=answer.id).count(),
                'predictions': Reply.objects.filter(
                    prediction=answer.id).count()
            })
        return results

    def get_location_results(self, question):
        location_votes = []
        location_results = []
        replies = [reply for reply in question.replies.all()]
        for reply in replies:
            location_vote = {
                'vote': reply.vote.id,
                'location': reply.user.profile.location
            }
            if location_vote in location_votes:
                index = location_votes.index(location_vote)
                location_results[index]['count'] += 1
            else:
                location_votes.append(location_vote)
                location_results.append({
                    'vote': reply.vote.id,
                    'location': reply.user.profile.location,
                    'count': 1
            })
        return location_results



class RecordSerializer(serializers.ModelSerializer):
    total_replies = serializers.SerializerMethodField()
    correct_predictions = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id',
            'total_replies',
            'correct_predictions'
        ]

    def get_total_replies(self, user):
        """
        Get the User's total number of Replies, excluding Replies to
        Questions that have not yet concluded.
        """
        total_replies = Reply.objects.filter(
            user=user,

            # The keyword below basically means
            # "question.date_concluded <= timezone.now()", to ensure
            # that we only consider Questions that have not yet
            # concluded.
            question__date_concluded__lte=timezone.now()

        ).count()
        return total_replies

    def get_correct_predictions(self, user):
        """
        Get the User's total number of Replies containing predictions
        that match the Question's Answer receiving the most votes,
        excluding Replies to Questions that have not yet concluded.
        """
        correct_predictions = 0
        replies = Reply.objects.filter(
            user=user,

            # The keyword below basically means
            # "question.date_concluded <= timezone.now()", to ensure
            # that we only consider Questions that have not yet
            # concluded.
            question__date_concluded__lte=timezone.now()

        ).all()
        for reply in replies:
            question = reply.question
            most_votes = 0
            top_answer = None
            for answer in question.answers.all():
                if answer.votes.count() > most_votes:
                    most_votes = answer.votes.count()
                    top_answer = answer
            if reply.prediction == top_answer:
                correct_predictions += 1
        return correct_predictions
