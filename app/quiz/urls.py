from django.urls import path
from quiz.views import QuizzesListView, QuestionsListView, QuestionView


app_name = 'quiz'

urlpatterns = [
    path('', QuizzesListView.as_view(), name='quizzes_list'),
    path('<str:title>', QuestionsListView.as_view(), name='questions_list'),
    path('<str:title>/questions', QuestionView.as_view(), name='question')
]
