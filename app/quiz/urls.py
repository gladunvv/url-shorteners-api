from django.urls import path
from quiz.views import QuizView, QuestionView


app_name = 'quiz'

urlpatterns = [
    path('', QuizView.as_view(), name='quiz_list'),
    path('<str:title>', QuestionView.as_view(), name='question')
]
