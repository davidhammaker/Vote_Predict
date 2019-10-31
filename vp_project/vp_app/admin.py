from django.contrib import admin
from .models import Question, Answer, Reply


class AnswerInLine(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'date_published',
        'date_concluded'
    ]
    inlines = [AnswerInLine]


class RepliesAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'vote', 'prediction')
    fields = [
        'user',
        'question',
        'vote',
        'prediction'
    ]
    list_filter = ('user', 'question')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, RepliesAdmin)
