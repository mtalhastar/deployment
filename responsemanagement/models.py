# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from questionaire.models import Questionnaire

class StudentResponses(models.Model):
    answer = models.TextField()
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    submitted = models.BooleanField(default=False)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, null=True, blank=True)
    testType=models.CharField(max_length=255,default='test1')
    def __str__(self):
        return self.answer

class ModelResponse(models.Model):
    answer = models.TextField()
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    severity_score=models.IntegerField()
    total=models.IntegerField(default=69)
    testType=models.CharField(max_length=255,default='test1')
    def __str__(self):
                 return self.answer