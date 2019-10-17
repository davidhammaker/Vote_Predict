from django.contrib import admin
from .models import Question, Answer


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


admin.site.register(Question, QuestionAdmin)
