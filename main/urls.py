from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('quiz/quiz-list', views.quiz_list, name='quiz_list'),
    path('quiz/create-quiz', views.create_quiz, name='create_quiz'),


]