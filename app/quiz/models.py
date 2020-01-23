from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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


class UserAnswer(models.Model):
    
    user = models.ForeignKey(User, related_name='user_answer', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'User Answer'
        verbose_name_plural = 'User Answers'

    def __str__(self):
        return f'User Answer on question: {self.answer}'
