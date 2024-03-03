from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    imageUrl=models.TextField(default='')

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen=models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']