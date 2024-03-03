from rest_framework import serializers
from .models import CriticalQuestionaire, Questionnaire


class QuestionSerializer(serializers.ModelSerializer):
    class Meta(object):
          model=Questionnaire
          fields=['id','title','questionnaire_type']

    
