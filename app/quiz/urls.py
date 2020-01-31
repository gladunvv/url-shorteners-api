from django.urls import path
from quiz.views import (
    StudentClassView,
    TeacherCabinetView,
    QuizzesListView,
    QuizDetailView,
    IndexView,
    TeacherQuizzesView,
    CreateQuizView,
    AddQuestionsView,
    AddAnswersView
)


app_name = 'quiz'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teacher/', TeacherCabinetView.as_view(), name='teacher_cabinet'),
    path('teacher/quizzes', TeacherQuizzesView.as_view(), name='teacher_quizzes'),
    path('create_quiz', CreateQuizView.as_view(), name='create_quiz'),
    path('<int:pk>/add_questions', AddQuestionsView.as_view(), name='add_questions'),
    path('<int:quiz_pk>/<int:question_pk>/add_answers', AddAnswersView.as_view(), name='add_answers'),
    path('student/', StudentClassView.as_view(), name='student_class'),
    path('list/', QuizzesListView.as_view(), name='quizzes_list'),
    path('<str:title>', QuizDetailView.as_view(), name='quiz_detail'),
]
