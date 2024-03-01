from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from . import serializers

@api_view(['GET'])
def quiz_detail_api(request, code):
    try:
        quiz = models.Quiz.objects.get(code=code)
    except models.Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.QuizDetailSerializer(quiz)
    return Response(serializer.data)



@api_view(['POST'])
def create_answers_api(request, code):
    try:
        quiz = models.Quiz.objects.get(code=code)
    except models.Quiz.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    # Serializer yaratish
    serializer = serializers.QuizTakerSerializer(data=request.data)
    if serializer.is_valid():
        # Ma'lumotlarni saqlash
        serializer.save(quiz=quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

