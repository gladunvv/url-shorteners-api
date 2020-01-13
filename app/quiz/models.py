from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Quiz(models.Model):

    title = models.CharField(max_length=60)
    description = models.TextField()
    success_text = models.TextField(blank=True)
    fail_text = models.TextField(blank=True)
    pass_mark = models.SmallIntegerField(
        validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
        ])
    
    class Meta:

        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f'Quiz: {self.title}'


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'Question: {self.text}'

class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=modles.CASCADE)
    variant = models.CharField()
    correct = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'Answer: {self.variant}'