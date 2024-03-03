from django.db import models
from django.contrib.auth.models import User


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    code = models.CharField()
    expiration_time = models.DateTimeField()
    
    class Meta:
        db_table = 'verification'
