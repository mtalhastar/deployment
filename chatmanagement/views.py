from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone
from responsemanagement.models import ModelResponse
from .models import Message,UserProfile
from .serializer import MessageSerializer,UserProfileSerializer
from .decorations import admin_required,student_required,is_psychologist_or_parent
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from asgiref.sync import async_to_sync
import datetime
from channels.layers import get_channel_layer
from django.utils import timezone
#getAllUserswithRespectToGroups
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getChatUsersWithSpecificGroups(request):
    newuser =User.objects.get(username=request.user.username)
    if newuser.groups.filter(name='Psychologist').exists():
       parents=User.objects.filter(groups__name='Parent')
       parent_profiles = UserProfile.objects.filter(user__in=parents)
       serializer = UserProfileSerializer(parent_profiles, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    elif newuser.groups.filter(name='Parent').exists():
       psychologists = User.objects.filter(groups__name='Psychologist')
       psychologist_profiles = UserProfile.objects.filter(user__in=psychologists)
       serializer = UserProfileSerializer(psychologist_profiles, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    else:
       return Response({'message':'You are not Authorized'},status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_psychologist_or_parent
def sendMessage(request,id):
   reciever_id=id
   content=request.data.get('content')
   sender_profile = get_object_or_404(UserProfile, user_id=request.user.id)
   receiver_profile = get_object_or_404(UserProfile, user_id=reciever_id)
   messageStatus=Message.objects.create(sender=sender_profile,receiver=receiver_profile,content=content) 
   print(messageStatus)
   current_time = datetime.datetime.now()
   print(current_time)
   if messageStatus:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{min(sender_profile.user.id, receiver_profile.user.id)}_{max(sender_profile.user.id, receiver_profile.user.id)}",
            {
                "type": "chat_message",
                "content": content,
                "senderid": sender_profile.user.id,
                "receiverid": receiver_profile.user.id,
                "seen":True,
                "timestamp":current_time
            }
        )
        messagestate=MessageSerializer(messageStatus)
        return Response({'message': messagestate.data}, status=status.HTTP_200_OK)
   return Response({'message':'You are not Authorized'},status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_psychologist_or_parent
def getMessages(request, id):
    receiver_id = id
    sender_profile = get_object_or_404(UserProfile, user_id=request.user.id)
    receiver_profile = get_object_or_404(UserProfile, user_id=receiver_id)

    # Fetch messages and mark them as seen if the logged-in user is the receiver
    messageStatus = Message.objects.filter(
        Q(sender=sender_profile, receiver=receiver_profile) | Q(sender=receiver_profile, receiver=sender_profile)
    ).order_by('-timestamp')

    # Update messages as seen if the logged-in user is the receiver
    if request.user.id == receiver_id:
        messageStatus.update(seen=True)

    # Serialize messages and return response
    messages = MessageSerializer(messageStatus, many=True)
    return Response({'conversation': messages.data}, status=status.HTTP_200_OK)
   
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_psychologist_or_parent
def deleteMessages(request,id):
   messageid=id
   message = Message.objects.filter(
      id=messageid
   )
   statusmessage =message.delete()
   if statusmessage[0]:
      return Response({'Success':'Deleted'},status=status.HTTP_200_OK)
   return Response({'message':'Error Deleting'},status=status.HTTP_400_BAD_REQUEST)  
   
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_psychologist_or_parent
def updateProfile(request):
   imageUri=request.data.get('image')
   username=request.data.get('username')
   sender_profile = get_object_or_404(UserProfile, user_id=request.user.id)
   if username:
        sender_profile.user.username = username
   if imageUri:
        sender_profile.imageUrl = imageUri
   sender_profile.save()
   return Response({'message':'Updated'},status=status.HTTP_200_OK)
   
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_psychologist_or_parent
def getProfile(request):
   sender_profile = get_object_or_404(UserProfile, user_id=request.user.id)
   if sender_profile:
    profile= UserProfileSerializer(sender_profile)
    return Response({'profile':profile.data},status=status.HTTP_200_OK)
   return Response({'message':"profile not found"},status=status.HTTP_404_NOT_FOUND)
   
    





