from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from quiz.models import Quiz, Question, Answer


class QuizzesListView(TemplateView):

    template_name = 'quiz/quiz_view.html'

    def get(self, request, *args, **qwargs):
        quiz = Quiz.objects.all()
        context = {
            'quiz': quiz
        }
        return render(request, self.template_name, context)


class QuestionsListView(TemplateView):

    template_name = 'quiz/questions_list_view.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(title=kwargs['title'])
        questions = quiz.questions.all()
        context = {
            'quiz': quiz,
            'questions': questions
        }
        return render(request, self.template_name, context)


class QuestionView(TemplateView):

    template_name = 'quiz/question_view.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(title=kwargs['title'])
        question = Question.objects.get(pk=kwargs['pk'])
        answers = question.answers.all()
        context = {
            'question': question,
            'answers': answers
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        answer = request.POST.get('answer')
        print(answer)
        return render(request, self.template_name   )