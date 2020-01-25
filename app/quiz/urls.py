from django.urls import path
from quiz.views import QuizzesListView, QuizDetailView, QuestionView, IndexView


app_name = 'quiz'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', QuizzesListView.as_view(), name='quizzes_list'),
    path('<str:title>', QuizDetailView.as_view(), name='quiz_detail'),
    path('<str:title>/questions', QuestionView.as_view(), name='question')
]
