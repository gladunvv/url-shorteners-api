from django.contrib import admin
from accounts.models import User


@admin.register(User)
class QuizAdmin(admin.ModelAdmin):
    pass