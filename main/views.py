from django.shortcuts import render, redirect
from main import models

def dashboard(request):
    quizs = models.Quiz.objects.all()
    context = {
        'quizs':quizs,
    }
    return render(request, 'dashboard/index.html', context)

def quiz_list(request):
    quizs = models.Quiz.objects.all()
    return render(request, 'dashboard/quiz/list.html', {'quizs':quizs})



def create_quiz(request):
    if request.method == 'POST':
        models.Quiz.objects.create(
            title=request.POST['title']
        )
        return redirect('quizs')
    return render(request, 'dashboard/quiz/create.html')
