from django.urls import path
from quiz.views import StudentClassView, TeacherCabinetView, QuizzesListView, QuizDetailView, IndexView


app_name = 'quiz'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teacher/', TeacherCabinetView.as_view(), name='teacher_cabinet'),
    path('student/', StudentClassView.as_view(), name='student_class'),
    path('list/', QuizzesListView.as_view(), name='quizzes_list'),
    path('<str:title>', QuizDetailView.as_view(), name='quiz_detail'),
]
