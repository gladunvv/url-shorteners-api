from django.contrib import admin
from quiz.models import Quiz, Question, Answer, StudentAnswer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Question)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(Answer)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')