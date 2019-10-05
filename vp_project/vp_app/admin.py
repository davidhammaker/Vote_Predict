from django.contrib import admin
from .models import Question, Answer


class AnswerInLine(admin.StackedInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'date_published'
    ]
    inlines = [AnswerInLine]


admin.site.register(Question, QuestionAdmin)
