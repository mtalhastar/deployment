# models.py

from django.db import models

class Questionnaire(models.Model):
    QUESTIONNAIRE_TYPES = (
        ('test1', 'Regular Questionnaire'),
        ('test2', 'Critical Questionnaire'),
    )
    title = models.CharField(max_length=255)
    questionnaire_type = models.CharField(max_length=10, choices=QUESTIONNAIRE_TYPES, blank=True, null=True)

    def __str__(self):
        return self.title


class CriticalQuestionaire(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
