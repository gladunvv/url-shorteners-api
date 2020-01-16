from django.views.generic import TemplateView
from django.shortcuts import render
from quiz.models import Quiz, Question, Answer


class QuizView(TemplateView):

    template_name = 'quiz/quiz_view.html'

    def get(self, request, *args, **qwargs):
        quiz = Quiz.objects.all()
        context = {
            'quiz': quiz
        }
        return render(request, self.template_name, context)


class QuestionView(TemplateView):

    template_name = 'quiz/question_view.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(title=kwargs['title'])
        questions = quiz.questions.all()
        context = {
            'quiz': quiz,
            'questions': questions
        }
        return render(request, self.template_name, context)
