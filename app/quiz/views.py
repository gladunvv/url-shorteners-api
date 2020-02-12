from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from quiz.models import Quiz, Question, Answer, StudentAnswer, TakenQuiz
from quiz.forms import QuestionForm, AnswerFormSet, TakeQuizForm
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            return redirect('quiz:student_permission_denied')
        return super(StudentRequiredMixin, self).dispatch(request, *args, **kwargs)


class TeacherRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('quiz:teacher_permission_denied')
        return super(TeacherRequiredMixin, self).dispatch(request, *args, **kwargs)


class StudentPermissionDenied(TemplateView):

    template_name = 'quiz/student_permission_denied.html'


class TeacherPermissionDenied(TemplateView):

    template_name = 'quiz/teacher_permission_denied.html'


class IndexView(TemplateView):

    template_name = 'quiz/index.html'


class StudentClassView(StudentPermissionDenied,TemplateView):

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


class TeacherCabinetView(TeacherRequiredMixin, ListView):

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


class TakeQuiz(CreateView):

    template_name = 'quiz/take_quiz_form.html'
    form_class = TakeQuizForm

    quiz = object = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        return super(TakeQuiz, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TakeQuiz, self).get_context_data(**kwargs)
        context['quiz'] = self.quiz
        context['question'] = self.get_question()
        context['progress'] = self.get_progress()

        return context

    def get_form_kwargs(self):
        kwargs = {
            'question': self.get_question(),
        }
        if self.request.method == 'POST':
            kwargs.update({
                'data': self.request.POST,
                'question': self.get_question(),
        })
        return kwargs

    def form_valid(self, form, **kwargs):
        student = self.request.user.student
        student_answer = form.save(commit=False)
        student_answer.user = student
        student_answer.save()
        if student.get_unanswered_questions(self.quiz).exists():
            return redirect('quiz:take_quiz', pk=self.quiz.pk)
        else:
            correct_answers = student.quiz_answers.filter(answer__question__quiz=self.quiz, answer__is_correct=True).count()
            score = round((correct_answers / self.get_total_questions()) * 100.0, 2)
            TakenQuiz.objects.create(student=student, quiz=self.quiz, score=score)
            if score < 50.0:
                messages.warning(self.request, 'Надеемся в дальнейшем вам повезёт больше! За викторину "{quiz}" вы заработали {score} баллов.' \
                    .format(quiz=self.quiz.title, score=score))
            else:
                messages.success(self.request, 'Поздравляем! Вы успешно закончили викторину "{quiz}"! Вы набрали {score} баллов!' \
                    .format(quiz=self.quiz.title, score=score))
            return redirect('quiz:quizzes_list')

    def get_total_questions(self):
        return self.quiz.questions.count()

    def get_progress(self):
        total_questions = self.get_total_questions()
        total_unanswered_questions = self.unanswered_questions().count()
        progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
        return progress

    def unanswered_questions(self):
        return self.request.user.student.get_unanswered_questions(self.quiz)

    def get_question(self):
        question = self.unanswered_questions().first()
        return question
