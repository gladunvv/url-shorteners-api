from django.contrib import admin
from quiz.models import Quiz, Question, Answer, UserAnswer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Question)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(Answer)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')