from django.db import models
from accounts.models import User


class Quiz(models.Model):

    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:

        verbose_name = 'Quiz'       
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f'Quiz: {self.title}'


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, related_name='questions',on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'Question: {self.text}'


class Answer(models.Model):

    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'Answer: {self.text}'


class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, blank=True, related_name='quizzes', on_delete=models.CASCADE)
    
    class Meta:

        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

        def __str__(self):
            return f'Teacher: {self.user.username}'


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')

    class Meta:

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'Student: {self.user.username}'


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, related_name='taken_quizzes', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='taken_quizzes', on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'Taken Quiz'
        verbose_name_plural = 'Taken Quizzes'

    def __str__(self):
        return f'Taken Quiz: {self.quiz}'


class StudentAnswer(models.Model):
    
    user = models.ForeignKey(Student, related_name='user_answer', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'User Answer'
        verbose_name_plural = 'User Answers'

    def __str__(self):
        return f'{self.answer}'
