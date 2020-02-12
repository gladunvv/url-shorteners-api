from django.urls import path
from quiz.views import (
    StudentClassView,
    TeacherCabinetView,
    QuizListView,
    QuizDetailView,
    IndexView,
    CreateQuizView,
    AddQuestionsView,
    AddAnswersView,
    TakenQuizListView,
    TakeQuiz,
    StudentPermissionDenied,
    TeacherPermissionDenied
)


app_name = 'quiz'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teacher/', TeacherCabinetView.as_view(), name='teacher_cabinet'),
    path('create_quiz', CreateQuizView.as_view(), name='create_quiz'),
    path('<int:pk>/add_questions', AddQuestionsView.as_view(), name='add_question'),
    path('<int:quiz_pk>/<int:question_pk>/add_answers', AddAnswersView.as_view(), name='add_answers'),
    path('student/', StudentClassView.as_view(), name='student_class'),
    path('list/', QuizListView.as_view(), name='quizzes_list'),
    path('quiz/<int:pk>', QuizDetailView.as_view(), name='quiz_detail'),
    path('taken_quiz', TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('student/quiz/<int:pk>', TakeQuiz.as_view(), name='take_quiz'),
    path('teacher/permission-denied', TeacherPermissionDenied.as_view(), name='teacher_permission_denied'),
    path('student/permission-denied', StudentPermissionDenied.as_view(), name='student_permission_denied'),
]
