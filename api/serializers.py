from rest_framework import serializers
from main import models

class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = models.Quiz
        fields = ['title', 'questions']

    def get_questions(self, obj):
        questions = models.Question.objects.filter(quiz=obj)
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['title', 'correct_answer']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['question', 'answer']

class QuizTakerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.QuizTaker
        fields = ['full_name', 'phone', 'email', 'answers']



class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = '__all__'

