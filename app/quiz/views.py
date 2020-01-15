from django.views.generic import TemplateView
from django.shortcuts import render
from quiz.models import Quiz


class QuizView(TemplateView):

    template_name = 'quiz/quiz_view.html'

    def get(self, request, *args, **qwargs):
        quiz = Quiz.objects.all()
        context = {
            'quiz': quiz
        }
        return render(request, self.template_name, context)


