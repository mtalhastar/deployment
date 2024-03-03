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
from .models import Questionnaire
from .serializer import QuestionSerializer
from .decorations import admin_required,student_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @admin_required
def getQuestionaire(request):
        questionnaires = Questionnaire.objects.all()
        serializedData = QuestionSerializer(questionnaires,many=True)
        return Response({'questionnaires': serializedData.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@student_required
def getStudentQuestions(request):
        existing_response = ModelResponse.objects.filter(studentid=request.user.id).first()  
        print(existing_response)
        if existing_response:
                if existing_response.testType=='test1':
                   questionnaires = Questionnaire.objects.filter(questionnaire_type='test2')
                   serializedData = QuestionSerializer(questionnaires,many=True)
                   return Response({'questionnaires': serializedData.data},status=status.HTTP_200_OK)
                elif existing_response.testType=='test2':
                   questionnaires = Questionnaire.objects.filter(questionnaire_type='test2')
                   serializedData = QuestionSerializer(questionnaires,many=True)
                   return Response({'questionnaires': serializedData.data},status=status.HTTP_200_OK)
                else:
                   return Response({'message:no other test'},status=status.HTTP_400_BAD_REQUEST)
        else:
                questionnaires = Questionnaire.objects.filter(questionnaire_type='test1')
                serializedData = QuestionSerializer(questionnaires,many=True)
                return Response({'questionnaires': serializedData.data},status=status.HTTP_200_OK)
     
       

@api_view(['GET'])
def updatestatus(request):
        Questionnaire.objects.all().update(questionnaire_type='test1')
        return Response({'updated'})

    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_required
def createQuestionaire(request):
        serializer=QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Questionaire cannot be created'})

@api_view(['DELETE']) 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_required
def delete(request,id):
        questionnaire = get_object_or_404(Questionnaire, pk=id)
        questionnaire.delete()
        return Response({'message': 'Questionnaire deleted successfully'})


@api_view(['DELETE']) 
@admin_required
def delete_all(request):
    questionnaires = Questionnaire.objects.all()
    
    if questionnaires.exists():
        questionnaires.delete()
        return Response({'message': 'All questionnaires deleted successfully'})
    else:
        return Response({'message': 'No questionnaires found to delete'})
    
@api_view(['PUT']) 
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_required
def updateQuestionaire(request,id):

        questionnaire = get_object_or_404(Questionnaire, pk=id)
        if not questionnaire:
         return Response({'message': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)
       
        updatedQuestionaire=QuestionSerializer(questionnaire,data=request.data)
       
        if updatedQuestionaire.is_valid():
           updatedQuestionaire.save()
           return Response({'message':'Questionaire updated'})
        return Response({'message': 'Questionnaire Failed to update'})
  