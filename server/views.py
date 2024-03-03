from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerialzier
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .helper import send_forgetPassword_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from random import randint
from datetime import datetime, timedelta
from django.utils import timezone
from .models import VerificationCode
import hashlib
from django.contrib.auth.models import Group
from .decorations import admin_required,student_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from chatmanagement.models import UserProfile
@api_view(['POST'])
def login(request):
    user =  User.objects.filter(email=request.data.get('email')).first()
    if not user.check_password(request.data['password']):
        return Response({"details":"Can't find details"},status=status.HTTP_404_NOT_FOUND)
    token,created=Token.objects.get_or_create(user=user)
    serializer= UserSerialzier(instance=user)
    user_group = user.groups.first()
    role = user_group.name if user_group else None
    
    return Response({"token":token.key,"serializer":serializer.data,"role":role})


@api_view(['POST'])
def signup(request):
    existing_user = User.objects.filter(email=request.data.get('email')).first()
    if existing_user:
        return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    serializer=UserSerialzier(data=request.data)
    if serializer.is_valid():
       serializer.save()
       user=User.objects.get(username=request.data['username'])
       #This builtin functions perform password hashing
       user.set_password(request.data["password"])       
       user.save()
       user_type = request.data.get("role")
       if user_type == 'admin':
            admin_group, created = Group.objects.get_or_create(name='Admin')
            admin_group.user_set.add(user)
       elif user_type == 'student':
            student_group, created = Group.objects.get_or_create(name='Student')
            student_group.user_set.add(user)
       elif user_type == 'psychologist':
            psychologist_group, created = Group.objects.get_or_create(name='Psychologist')
            psychologist_group.user_set.add(user)
            UserProfile.objects.create(user=user,group=psychologist_group)
       elif user_type == 'parent':
            parent_group, created = Group.objects.get_or_create(name='Parent')
            parent_group.user_set.add(user)
            UserProfile.objects.create(user=user,group=parent_group)
       token = Token.objects.create(user=user)
       return Response({"token":token.key,"user":serializer.data,"role":user.groups.first().name},status=status.HTTP_200_OK)
    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def changePassword(request):
    
    vcode = request.data["vcode"]
    password= request.data["password"]
    if not vcode or not password:
        return Response({"message": "Verification Code or Password is Missing"}, status=status.HTTP_400_BAD_REQUEST)
   
    hashed_provided_code = hashlib.sha256(vcode.encode()).hexdigest()
    verification_instance = VerificationCode.objects.filter(code=hashed_provided_code).first()
   
    if not verification_instance:
        return Response({"message":"Verfication code is incorrect"},status=status.HTTP_404_NOT_FOUND)
    
    if verification_instance and verification_instance.expiration_time > timezone.now():
         user= User.objects.get(username=verification_instance.user.username)
         user.set_password(password)
         user.save()
         verification_instance.delete()
         return Response({"message": "Password reset successful"})
    if verification_instance.expiration_time < timezone.now():
         return Response({"message": "The code is expired"},status=status.HTTP_403_FORBIDDEN)
    return Response({"message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgetPassword(request):
    
    user =  User.objects.filter(email=request.data.get('email')).first()
    print(user.email)
    if not user:
        return Response({"message":"Can't find User"},status=status.HTTP_404_NOT_FOUND)
    user_obj=User.objects.get(username=user.username)
    token,_ = Token.objects.get_or_create(user=user) 
    verificationCode = str(randint(100000, 999999))
    expiration_time = timezone.now() + timedelta(minutes=10)
    hashed_verification_code = hashlib.sha256(verificationCode.encode()).hexdigest()
    print(user)
    # Create a VerificationCode instance and save it to the database
    VerificationCode.objects.create(
        user=user_obj,
        email=user_obj.email,
        code=hashed_verification_code,
        expiration_time=expiration_time
    )
    send_forgetPassword_mail(user_obj.email,verificationCode)
    return Response({"message":"Password Link Sent To Your Email","token":token.key})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the user's authentication token to log them out
    try:
        request.auth.delete()
    except (AttributeError, Token.DoesNotExist):
        pass  # If token doesn't exist or has already been deleted, just continue
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)



@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @admin_required
def get_all_users(response):
    users = User.objects.all()
    user_list = []  
    
    for user in users:
        user_data = {
            'username': user.username,
            'email': user.email,
            'id':user.id,
             'roles': list(user.groups.values_list('name', flat=True)) 
        }
        user_list.append(user_data)
    return Response({'users': user_list})


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_required
def delete_user_by_id(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return Response({'message': f'User with ID {id} has been deleted'}, status=status.HTTP_204_NO_CONTENT)


