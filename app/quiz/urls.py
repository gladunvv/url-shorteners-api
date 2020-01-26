from django.urls import path
from quiz.views import QuizzesListView, QuizDetailView, IndexView


app_name = 'quiz'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', QuizzesListView.as_view(), name='quizzes_list'),
    path('<str:title>', QuizDetailView.as_view(), name='quiz_detail'),
]
