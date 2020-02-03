from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls'), name='quiz'),
    path('accounts/', include('accounts.urls'), name='accounts'),
]
