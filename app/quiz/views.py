from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from quiz.models import Quiz, Question, Answer, UserAnswer


class IndexView(TemplateView):

    template_name = 'quiz/index.html'


class QuizzesListView(TemplateView):

    template_name = 'quiz/quiz_view.html'

    def get(self, request, *args, **qwargs):
        quizzes = Quiz.objects.all()
        context = {
            'quizzes': quizzes
        }
        return render(request, self.template_name, context)


class QuizDetailView(TemplateView):

    template_name = 'quiz/quiz_detail.html'

    def get(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, title=kwargs['title'])
        context = {
            'quiz': quiz
        }
        return render(request, self.template_name, context)

