from django.urls import path
from quiz.views import QuizView


app_name = 'quiz'

urlpatterns = [
    path('', QuizView.as_view(), name='quiz')   
]
