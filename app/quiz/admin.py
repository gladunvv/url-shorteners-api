from django.contrib import admin
from quiz.models import Quiz, Question, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'pass_mark')


@admin.register(Question)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(Answer)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('variant', 'correct')