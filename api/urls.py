from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('quiz/', views.quiz_list, name='quiz-list'),
    path('question/', views.question_list, name='question-list'),
    path('answer/', views.answer_list, name='answer-list'),
    path('quiztaker/', views.quiztaker_list, name='quiztaker-list'),
]


              