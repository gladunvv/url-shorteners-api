from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from quiz.models import Quiz, Question, Answer, StudentAnswer, TakenQuiz
from quiz.forms import QuestionForm, AnswerFormSet, TakeQuizForm
from django.db.models import Count


class IndexView(TemplateView):

    template_name = 'quiz/index.html'


class StudentClassView(TemplateView):

    template_name = 'quiz/student_class.html'


class CreateQuizView(CreateView):

    model = Quiz
    fields = ['title', 'description']
    template_name = 'quiz/create_quiz.html'
    
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.teacher = self.request.user.teacher
        quiz.save()
        return redirect('quiz:add_question', pk=quiz.id)


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


class TeacherCabinetView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/teacher_cabinet.html'

    def get_queryset(self):
        queryset = self.request.user.teacher.quizzes.annotate(questions_count=Count('questions', distinct=True))
        return queryset


class QuizDetailView(DetailView):

    model = Quiz
    template_name = 'quiz/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=context['quiz'])
        return context


class QuizListView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quiz/quiz_view.html'

    def get_queryset(self):
        student = self.request.user.student
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.all() \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


class TakenQuizListView(ListView):

    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quiz/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz') \
            .order_by('quiz__title')
        return queryset



class TakeQuizView(CreateView):
    
    form_class = TakeQuizForm
    template_name = 'quiz/take_quiz_form.html'


    quiz = object = None
    total_questions = object = None
    unanswered_questions = object = None
    total_unanswered_questions = object = None
    progress = object = None
    question = object = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        self.total_questions = self.quiz.questions.count()
        self.unanswered_questions = request.user.student.get_unanswered_questions(self.quiz)
        self.total_unanswered_questions = self.unanswered_questions.count()
        self.progress = 100 - round(((self.total_unanswered_questions - 1) / self.total_questions) * 100)
        self.question = self.unanswered_questions.first()
        return super(TakeQuizView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TakeQuizView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(question=self.question)
        context['question'] = self.question
        context['quiz'] = self.quiz
        context['progress'] = self.progress
        return context

    def get(self, request, *args, **kwargs):

        if self.request.user.student.quizzes.filter(pk=kwargs['pk']).exists():
            return render(request, 'quiz/taken_quiz_list.html')

    def post(self, request, *args, **kwargs):
        student = request.user.student
        form = self.form_class(question=self.question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(self.quiz).exists():
                    return redirect('quiz:take_quiz', kwargs['pk'])
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=self.quiz, answer__is_correct=True).count()
                    score = round((correct_answers / self.total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=self.quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (self.quiz.title, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (self.quiz.title, score))
                    return redirect('quiz:quzzes_list')

