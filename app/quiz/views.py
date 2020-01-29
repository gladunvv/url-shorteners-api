from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from quiz.models import Quiz, Question, Answer, StudentAnswer
from quiz.forms import QuestionForm

from django.db.models import Count

class IndexView(TemplateView):

    template_name = 'quiz/index.html'


class StudentClassView(TemplateView):

    template_name = 'quiz/student_class.html'


class TeacherCabinetView(TemplateView):

    template_name = 'quiz/teacher_cabinet.html'

class CreateQuizView(CreateView):

    model = Quiz
    fields = ['title', 'description']
    template_name = 'quiz/create_quiz.html'
    
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.teacher = self.request.user.teacher
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('quiz:add_questions', pk=quiz.id)



class AddQuestionsView(CreateView):
    
    form_class = QuestionForm
    template_name = 'quiz/add_question.html'
    
    quiz = object = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'], teacher=request.user.teacher)

        return super(AddQuestionsView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        question = form.save(commit=False)
        question.quiz = self.quiz
        question.save()
        return redirect('quiz:teacher_quizzes')



class TeacherQuizzesView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/teacher_quizzes.html'

    def get_queryset(self):
        queryset = self.request.user.teacher.quizzes.annotate(questions_count=Count('questions', distinct=True))
        return queryset



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

