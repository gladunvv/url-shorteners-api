from django.core.paginator import Paginator
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

    # def post(self, requset, *args, **kwargs):
    #     quiz = Quiz.objects.get(title=kwargs['title'])


class QuestionView(TemplateView):

    template_name = 'quiz/question_view.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(title=kwargs['title'])
        question = Question.objects.filter(quiz=quiz)


        paginator = Paginator(question, 1)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
        
    #     answer = request.POST.get('answer')
    #     quiz = Quiz.objects.get(title=kwargs['title'])
    #     question = Question.objects.get(pk=kwargs['pk'])
        
    #     return render(request, self.template_name   )
