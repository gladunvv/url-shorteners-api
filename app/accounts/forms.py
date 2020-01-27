from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from quiz.models import Student, Teacher


class MyUserCreationForm(UserCreationForm):
    is_student = forms.BooleanField(required=False, initial=False)
    is_teacher = forms.BooleanField(required=False, initial=False)
    
    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        cleaned_data = super(StudentCreationForm, self).clean()
        is_student = cleaned_data.get("is_student")
        is_teacher = cleaned_data.get("is_teacher")
        if is_teacher and is_student:
            self._errors['is_student'] = self.error_class([ 
                'Enter only one of teacher or student']) 
        elif not is_student and not is_teacher:
            self._errors['is_teacher'] = self.error_class([ 
                'You must enter a teacher or a student']) 
        return cleaned_data

    def save(self):
        user = super().save(commit=False)
        is_student = self.cleaned_data.get("is_student")
        is_teacher = self.cleaned_data.get("is_teacher")
        if is_student:  
            user.is_student = True
            user.save()
            student = Student.objects.create(user=user)
        if is_teacher:
            user.is_teacher = True
            user.save()
            teacher = Teacher.objects.create(user=user)
        return user
