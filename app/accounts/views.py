from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm

from accounts.forms import TeacherCreationForm, StudentCreationForm

class StudentSignUpView(TemplateView):

    template_name = 'accounts/signup_student.html'

    def get(self, request, *args, **kwargs):
        form = StudentCreationForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

class TeacherSignUpView(TemplateView):

    template_name = 'accounts/signup_teacher.html'

    def get(self, request, *args, **kwargs):
        form = TeacherCreationForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogInView(TemplateView):

    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
                )
            login(request, user)
            return redirect('quiz:index')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogOutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')
