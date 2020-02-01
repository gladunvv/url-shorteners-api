from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from quiz.models import Quiz, Question, Answer, StudentAnswer
from quiz.forms import QuestionForm, AnswerFormSet

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
        return redirect('quiz:add_answers', quiz_pk=self.quiz.id, question_pk=question.id)


class AddAnswersView(CreateView):

    form_class = QuestionForm
    template_name = 'quiz/add_answers.html'
    
    quiz = object = None
    question = object = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['quiz_pk'], teacher=request.user.teacher)
        self.question = get_object_or_404(Question, pk=kwargs['question_pk'], quiz=self.quiz)
        return super(AddAnswersView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddAnswersView, self).get_context_data(**kwargs)
        context['formset'] = AnswerFormSet(instance=self.question)
        context['form'] = self.form_class(instance=self.question)
        context['quiz'] = self.quiz
        context['question'] = self.question
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST, instance=self.question)
        formset = AnswerFormSet(self.request.POST, instance=self.question)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.get_context_data

    def form_valid(self, form, formset):
        with transaction.atomic():
            form.save()
            formset.save()
        return redirect('quiz:quiz_detail', pk=self.quiz.id)


class TeacherQuizzesView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/teacher_quizzes.html'

    def get_queryset(self):
        queryset = self.request.user.teacher.quizzes.annotate(questions_count=Count('questions', distinct=True))
        return queryset



class QuizzesListView(ListView):

    model = Quiz
    template_name = 'quiz/quiz_view.html'


class QuizDetailView(DetailView):

    model = Quiz
    template_name = 'quiz/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=context['quiz'])
        return context