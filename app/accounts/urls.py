from django.urls import path
from accounts.views import TeacherSignUpView, StudentSignUpView, LogInView, LogOutView


app_name = 'accounts'

urlpatterns = [
    path('signup-teacher/', TeacherSignUpView.as_view(), name='signup_teacher'),
    path('signup-student/', StudentSignUpView.as_view(), name='signup_student'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout')
]
