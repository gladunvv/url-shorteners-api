from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

class Quiz(models.Model):

    user = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField()
    success_text = models.TextField(blank=True)
    normal_text = models.TextField(blank=True)
    fail_text = models.TextField(blank=True)

    class Meta:

        verbose_name = 'Quiz'       
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f'Quiz: {self.title}'


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, related_name='questions',on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'Question: {self.text}'


class Answer(models.Model):

    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    variant = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'Answer: {self.variant}'


class UserAnswer(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'User Answer'
        verbose_name_plural = 'User Answers'

    def __str__(self):
        return f'User Answer on {question}: {answer}'
