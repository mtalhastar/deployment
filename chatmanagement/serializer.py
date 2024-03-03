from rest_framework import serializers
from .models import UserProfile, Message


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    role = serializers.ReadOnlyField(source='group.name')
    class Meta(object):
          model=UserProfile
          fields=['id','imageUrl','user','username','email','role']

class MessageSerializer(serializers.ModelSerializer):
    senderid = serializers.ReadOnlyField(source='sender.user.id')
    receiverid = serializers.ReadOnlyField(source='receiver.user.id')
    class Meta(object):
          model=Message
          fields=['id','content','seen','senderid','receiverid','timestamp']