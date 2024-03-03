from rest_framework import serializers
from .models import StudentResponses
from .models import ModelResponse

class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta(object):
          model=StudentResponses
          fields='__all__'

    

class ModelResponseSerializer(serializers.ModelSerializer):
    class Meta(object):
          model=ModelResponse
          fields='__all__'