from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from . import serializers
from rest_framework.renderers import JSONRenderer


@api_view(['GET'])
def quiz_list(request):
    quizzes = models.Quiz.objects.all()
    serializer = serializers.QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def question_list(request):
    questions = models.Question.objects.all()
    serializer = serializers.QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def answer_list(request):
    answers = models.Answer.objects.all()
    serializer = serializers.AnswerSerializer(answers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def quiztaker_list(request):
    quiztakers = models.QuizTaker.objects.all()
    serializer = serializers.QuizTakerSerializer(quiztakers, many=True)
    return Response(serializer.data)
