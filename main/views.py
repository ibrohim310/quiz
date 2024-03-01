from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse

# Create your views here.
@login_required(login_url = 'dash:login')
def main(request):
    quizes = Quiz.objects.filter(author = request.user)
    context = {
        "quizes" : quizes
    }
    return render(request, 'main.html', context)

@login_required(login_url = 'dash:login')
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        quiz = Quiz.objects.create(
            title = title,
            author = request.user
        )
        return redirect('dash:quest_create', quiz.id)
    return render(request, 'quiz/create-quiz.html')

#@login_required(login_url = 'dash:login')
#def create_question(request, id):
#    quiz = Quiz.objects.get(id = id)
#    if request.method == 'POST':
#        
#        title = request.POST['title']
#        ques = Question.objects.create(
#            quiz = quiz,
#            title = title
#        )
#        Option.objects.create(
#            question = ques,
#            name = request.POST['correct'],
#            is_correct = True
#        )
#        data = [request.POST['incorrect1'], request.POST['incorrect2'], request.POST['incorrect3']]
#
#        for i in data:
#            Option.objects.create(
#                question = ques,
#                name = i,
#            )
#        if request.POST['submit_action'] == 'exit':
#            return redirect('dash:main')
#
#    return render (request, 'quiz/create-question.html' )


@login_required(login_url='dash:login')
def create_question(request, id):
    quiz = Quiz.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        correct_answer = request.POST.get('correct', '')
        if title and correct_answer:
            # Create the question
            question = Question.objects.create(quiz=quiz, title=title)
            
            # Create the correct option
            Option.objects.create(question=question, name=correct_answer, is_correct=True)
            
            # Create incorrect options
            for i in range(1, 11):  # Assuming maximum 10 incorrect options
                incorrect_option = request.POST.get(f'incorrect{i}', '')
                if incorrect_option:
                    Option.objects.create(question=question, name=incorrect_option)
            
            if request.POST.get('submit_action') == 'exit':
                return redirect('dash:main')

    return render(request, 'quiz/create-question.html')



@login_required(login_url = 'dash:login')
def questions_list(request, id):
    quests = Question.objects.filter(quiz_id = id)
    context = {
        'questions': quests
    }
    return render (request, 'details/questions.html', context)

#@login_required(login_url = 'dash:login')
#def quest_detail(request, id):
#    question = Question.objects.get(id = id)
#    option_correct = Option.objects.get(question = question, is_correct = True)
#    options = Option.objects.filter(question = question, is_correct = False).order_by('id')
#    context = {
#        'question': question,
#        'options': options,
#        'option_correct' : option_correct
#    }
#    if request.method == 'POST':
#        question.title = request.POST['title']
#        question.save()
#
#        option_correct.name = request.POST['correct']
#        option_correct.save()
#
#        data = [request.POST['incorrect1'], request.POST['incorrect2'], request.POST['incorrect3']]
#
#        for i, opt in enumerate(options):
#            opt.name = data[i]
#            opt.save()
#    return render( request, 'details/detail.html', context)


@login_required(login_url='dash:login')
def quest_detail(request, id):
    question = Question.objects.get(id=id)
    option_correct = Option.objects.get(question=question, is_correct=True)
    options = Option.objects.filter(question=question, is_correct=False).order_by('id')
    context = {
        'question': question,
        'options': options,
        'option_correct': option_correct
    }
    if request.method == 'POST':
        title = request.POST.get('title', '')
        correct = request.POST.get('correct', '')
        incorrects = [request.POST.get(f'incorrect{i}', '') for i in range(1, 11)]  # 11 - Max incorrect answers
        if title:
            question.title = title
            question.save()
        if correct:
            option_correct.name = correct
            option_correct.save()
        for index, option in enumerate(options):
            if index < len(incorrects):
                incorrect = incorrects[index]
                if incorrect:
                    option.name = incorrect
                    option.save()
            else:
                break  # Stop iterating if there are no more incorrect answers provided
        if request.POST.get('submit_action') == 'exit':
            return redirect('dash:main')
    return render(request, 'details/detail.html', context)



@login_required(login_url = 'dash:login')
def quiz_delete(request, id):
    Quiz.objects.get(id = id).delete()
    return redirect('dash:main')



@login_required(login_url = 'dash:login')
def get_results(request, id):
    quiz = Quiz.objects.get(id=id)
    taker = QuizTaker.objects.filter(quiz=quiz)

    # results = []
    # for i in taker:
    #     results.append(Result.objects.get(taker=i))
    
    results = tuple(
            map(
            lambda x : Result.objects.get(taker=x),
            taker
        )
    )
    return render(request, 'quiz/results.html', {'results':results})

def result_detail(request, id):
    result = Result.objects.get(id=id)
    answers = Answer.objects.filter(taker=result.taker)
    context = {
        'taker':result.taker,
        'answers':answers
    }
    return render(request, 'quiz/result-detail.html', context)



#login


def logging_in(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(username = username, password=password)
        if user:
            login(request, user)
            return redirect('dash:main')
        else:
            status = 'incorrect username or password'
    return render(request, 'auth/login.html', {'status':status})

def register(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).first():
            User.objects.create_user(
                username=username,
                password=password
            )
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('dash:main')
        else:
            status  = f'the username {username} is occupied'
    return render(request, 'auth/register.html', {'status': status})


#export excel


def export_results(request):
    results = Result.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="quiz_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['FIO', 'Telefon', 'Email', 'Jami savollar', 'Togri javoblar', 'Notogri javoblar', 'Foiz'])

    for result in results:
        writer.writerow([
            result.taker.full_name,
            result.taker.phone,
            result.taker.email,
            result.questions,
            result.correct_answers,
            result.incorrect_answers,
            result.percentage
        ])

    return response
