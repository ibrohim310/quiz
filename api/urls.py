from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('api/quiz-detail/<str:code>/', views.quiz_detail_api, name='quiz-detail-api'),
    path('api/quiz/<str:code>/create-answers/', views.create_answers_api, name='create-answers-api'),
]
              