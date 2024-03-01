from rest_framework import serializers
from main import models

class QuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = ['title', 'correct_answer', 'options']

    def get_correct_answer(self, question):
        correct_answer = question.correct_answer
        if correct_answer:
            return correct_answer.name
        return None

    def get_options(self, question):
        options = question.get_options()
        return [option.name for option in options]


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Quiz
        fields = ['title', 'questions']



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['question', 'answer']

class QuizTakerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.QuizTaker
        fields = ['full_name', 'phone', 'email', 'answers']

