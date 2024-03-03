import re
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
from .models import StudentResponses,ModelResponse
from questionaire.models import Questionnaire
from .serializer import StudentResponseSerializer,ModelResponseSerializer
import speech_recognition as sr
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from .decorations import *
import openai
from .mindcarebot import *

apiKey = ''
openai.api_key = apiKey

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_required
def getAllStudentResponses(request):   
        reponses = StudentResponses.objects.all()
        serializedData = StudentResponseSerializer(reponses,many=True)
        return Response({'responses': serializedData.data})
    
    
@api_view(['DELETE'])
def deleteAllStudentResponses(request):
          responses=StudentResponses.objects.all()
          if responses.exists():
              responses.delete()
          return Response({'responses': responses})
      
      
@api_view(['GET'])
def filteredStudents(request):
    # Get the 'score' parameter from the request data
    # score = request.data.get("score")
    # Check if 'score' is present in the request data
    # if score:
        # Severity Threshold
        scoreOftest1 = 30
        scoreOftest2 = 45
        # Filter ModelResponse objects where severity_score is greater than or equal to 'score'
        filtered_responses = ModelResponse.objects.filter(severity_score__gte=scoreOftest1,testType='test1')
        filtered_responses_for_secondtest = ModelResponse.objects.filter(severity_score__gte=scoreOftest2,testType='test2')
        # Extract relevant information for response
        response_data = [
                {
                    'answer': response.answer+'\n'+f'Total Score: {response.severity_score}',
                    'studentid': response.studentid.id,
                    'username': response.studentid.username,
                    'email': response.studentid.email,
                    'timestamp': response.timestamp,
                    'severity_score': response.severity_score,
                     'testType':'Test-1',
                     'total':response.total
                }
                for response in filtered_responses
            ] + [
                {
                    'answer': response.answer+'\n'+f'Total Score: {response.severity_score}',
                    'studentid': response.studentid.id,
                    'username': response.studentid.username,
                    'email': response.studentid.email,
                    'timestamp': response.timestamp,
                    'severity_score': response.severity_score,
                    'testType':'Test-2',
                     'total':response.total
                }
                for response in  filtered_responses_for_secondtest
            ]
        
        return Response(response_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])   
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated]) 
# @admin_required 
def getAllAIResponses(request):   
    responses = ModelResponse.objects.all()
    serialized_data = []
    
    for response in responses:
        response_data = ModelResponseSerializer(response).data
        response_data['username'] = response.studentid.username
        response_data['email'] = response.studentid.email
        serialized_data.append(response_data)

    return Response({'responses': serialized_data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])     
def deleteSpecificResponse(request, id):   
    # Try to get the response with the specified ID
    response = get_object_or_404(ModelResponse, id=id)
    # Delete the response
    response.delete()
    return Response({'message': 'Response deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@student_required
def testIfResponseSubmitted(request):
      existing_response = ModelResponse.objects.filter(studentid=request.user.id,testType='test1').first()
      print('t1',existing_response) 
      existing_response_2 = ModelResponse.objects.filter(studentid=request.user.id,testType='test2').first()
      print('t2',existing_response_2)   
      if existing_response_2:
            return Response({'message': 'All tests are submitted'}, status=status.HTTP_400_BAD_REQUEST)
      elif existing_response:
            return Response({'message': 'Test-2 Started'}, status=status.HTTP_200_OK)
      else:
        return Response({'message': 'Test Started'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@student_required
def getAStudentResponse(request):
    
        student_instance = request.user
        newscore= request.data.get('score',None)
        student_detail=request.data.get('studentdetails',None)
        
        if not student_instance:
           return Response({'error': 'Student DoesNot exist'}, status=status.HTTP_404_NOT_FOUND)
        questionaire = Questionnaire.objects.filter(questionnaire_type='test1')
        
        secondTestisTaken = ModelResponse.objects.filter(studentid=student_instance.id,testType='test2').first()
        if secondTestisTaken:
            return Response({'message':'All tests are taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        questionairetwo = Questionnaire.objects.filter(questionnaire_type='test2')
        firstTestIsTaken = ModelResponse.objects.filter(studentid=student_instance.id,testType='test1').first()
        if firstTestIsTaken:
                firstTestIsTaken.testType='test2'
                firstTestIsTaken.severity_score=newscore
                firstTestIsTaken.answer=student_detail
                firstTestIsTaken.total=len(questionairetwo)*3
                firstTestIsTaken.save()
                return Response({'message': 'Test is submitted'}, status=status.HTTP_200_OK)
                
                
        student_responses = StudentResponses.objects.filter(studentid=student_instance.id,testType='test1')
        response_data = []
        skipped_questions = []

        for i, questionnaire in enumerate(questionaire):
         response = student_responses.filter(questionnaire=questionnaire).first()

         if not response:
            skipped_questions.append(f"{i + 1}")

        if skipped_questions:
         return Response({'message': f'Please respond to remaining questions {", ".join(skipped_questions)}'}, status=status.HTTP_400_BAD_REQUEST)

        all_response = ""
        for i in range(len(student_responses)): 
         all_response +="Q"+ str(i+1)+": "+ student_responses[i].questionnaire.title + "\n Answer: " + student_responses[i].answer + "\n"
        #ai response score extract
    
    
        for i in range(len(student_responses)):
         stress = "Stress (1-5)"
         anxiety = "Anxiety (6-10)"
         depression = "Depression (11-15)"
         if i==0:
             response_data.append(stress)
         if i==5:  
             response_data.append(anxiety)
         if(i==10):
             response_data.append(depression)     
         response_data.append({   
            'question': str(i+1)+"- "+student_responses[i].questionnaire.title,
            'Answer': " "+student_responses[i].answer,
        })
         
        print(response_data)
        conversation = [
            {"role": "user", "content": Instructions + '''
             Please find below the patient's responses to the psychological questions: 
             '''+ str(response_data) +
             Criteria},
        ]

        airesponse = MindCareModel(conversation)
        print(airesponse)
        conversation1 = [
                {"role": "system", "content": "Calculate the total score based on the GAD-7, PHQ-9, and Perceived Stress Scale (PSS) criteria."},
                {"role": "user", "content": airesponse},
                {"role": "system", "content": "From the study above, give only the total score which is the sum of all the scores, STRICTLY in this format: Score = Total score of all 3 criterias out of 45. For example Score = 15."},
        ]

        score = MindCareModel(conversation1)
        print(score)
        severity_Score=extract_severity_score(score)
        print(severity_Score)
      
        
        if severity_Score:
         existing_response = ModelResponse.objects.filter(studentid=student_instance.id).first()
         print(existing_response)
         if existing_response:
            existing_response.answer = all_response+"\n"+airesponse
            existing_response.severity_score = severity_Score
            existing_response.save()
            modelserializer= ModelResponseSerializer(existing_response)
            return Response({'response': modelserializer.data}, status=status.HTTP_200_OK)
         airesponsedata = {'answer':'Test-1 \n'+all_response+"\n"+airesponse, 'studentid': student_instance.id,'severity_score': severity_Score,'total':len(student_responses)*3}
         modelserializer= ModelResponseSerializer(data=airesponsedata)
         if modelserializer.is_valid():
             modelserializer.save()
         else:
             print(modelserializer.errors)
             print('response not saved') 
        else:
          #Email will be sent to give test again,Responses werent correct
          return Response({'message': 'We found some of your responses irrelevent'}, status=status.HTTP_400_BAD_REQUEST)  
        if not student_responses:
            return Response({'error': 'Student doesnt exit'}, status=status.HTTP_404_NOT_FOUND)
        # serializedData = StudentResponseSerializer(student_responses, many=True)
        return Response({'responses': response_data}, status=status.HTTP_200_OK)
    
    
def MindCareModel(Conversation):

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=Conversation,
            max_tokens=2000,  
        )
    generated_response = response.choices[0].message["content"]
    return generated_response


def performCriticalAnalysis(student_responses,questionaire,studentid):
    response_data = []
    skipped_questions = []

    for i, questionnaire in enumerate(questionaire):
        response = student_responses.filter(questionnaire=questionnaire).first()

        if not response:
           skipped_questions.append(f"{i + 1}")

    if skipped_questions:
            return Response({'message': f'Please respond to remaining questions {", ".join(skipped_questions)}'}, status=status.HTTP_400_BAD_REQUEST)

    all_response = ""
    for i in range(len(student_responses)): 
                 all_response +="Q"+ str(i+1)+": "+ student_responses[i].questionnaire.title + "\n Answer: " + student_responses[i].answer + "\n"
                 
    for i in range(len(student_responses)):
         stress = "Stress (1-3)"
         anxiety = "Anxiety (4-5)"
         depression = "Depression (6-8)"
         if i==0:
             response_data.append(stress)
         if i==3:  
             response_data.append(anxiety)
         if(i==5):
             response_data.append(depression)     
         response_data.append({   
            'question': str(i+1)+"- "+student_responses[i].questionnaire.title,
            'Answer': " "+student_responses[i].answer,
        })
         
    print(response_data)
    conversation = [
            {"role": "user", "content": INSTRUCTIONS1 + '''
             Please find below the patient's responses to the psychological questions: 
             '''+ str(response_data) +
             Criteria2},
        ]

    airesponse = MindCareModel(conversation)
    print(airesponse)
    conversation1 = [
                {"role": "system", "content": "Calculate the total score"},
                {"role": "user", "content": airesponse},
                {"role": "system", "content": "From the study above, give only the total score which is the sum of all the scores, STRICTLY in this format: Score = Total score out of 24. For example Score = 15."},
            ]

    score = MindCareModel(conversation1)
    print(score)
    severity_Score=extract_severity_score(score)
    print(severity_Score)
      
    if severity_Score:
         existing_response = ModelResponse.objects.filter(studentid=studentid).first()
         print(existing_response)
         if existing_response:
            existing_response.answer =existing_response.answer+'\n Test-2 \n' +all_response+"\n"+airesponse
            existing_response.severity_score = severity_Score
            existing_response.total=len(student_responses)*3
            existing_response.save()
            modelserializer= ModelResponseSerializer(existing_response)
            return Response({'response': modelserializer.data}, status=status.HTTP_200_OK)
    else:
          #Email will be sent to give test again,Responses werent correct
          return Response({'message': 'We found some of your responses irrelevent'}, status=status.HTTP_400_BAD_REQUEST)  
    if not student_responses:
            return Response({'error': 'Student doesnt exit'}, status=status.HTTP_404_NOT_FOUND)
        #ai response score extract
    
    
    
# def getScore(conversation):
#     # Add a user prompt to get the severity score and comments
#     score_prompt = "Based on the analysis provided before, please give me the severity score for the patient's mental health. The score should be a sum of the total score. It should be printed in this manner: 'Score = The total Score calculated'. For example Score = 15. Please follow it strictly. Additionally, comment on any detected mental health concerns and provide reasons for these concerns as per the patient's responses."
    
#     # Continue the conversation
#     conversation.append({"role": "user", "content": score_prompt})
    
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=conversation,
#         max_tokens=1000,
#     )
    
#     response_content = response.choices[0].message["content"]
#     print(response_content)
#     return response_content

# Use the conversation history for the severity score
def extract_severity_score(text):
    # Check if the string starts with "Score"
    if text.startswith("Score"):
        # Extract all numbers following the "Score" keyword
        numbers = re.findall(r'\b(\d+)\b(?![^(]*\))', text)

        # If there is an explicit total at the end, use that
        total_match = re.search(r'=\s*(\d+)\s*$', text)
        if total_match:
            return int(total_match.group(1))
        
        # Otherwise, sum up all the extracted numbers
        if numbers:
            total_score = sum(map(int, numbers))
            return total_score

    return None

@api_view(['POST'])
def saveStudentResponse(request,id):
    # Check if 'audio_file' is present in the request
    audio_file = request.FILES.get('audio_file')
    if not audio_file:
        return Response({'error': 'Audio file not provided'}, status=status.HTTP_400_BAD_REQUEST)
    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    print(1)
    try:
        # Load audio file and recognize speech
        print('2')
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            print('Analysing Audio')
            text = recognizer.recognize_google(audio_data)  # You can use other speech-to-text engines too
            print(text)
        student_instance = User.objects.get(id=id)
        if not student_instance:
           return Response({'error': 'Student DoesNot exist'}, status=status.HTTP_404_NOT_FOUND)
        # Create a dictionary with the recognized text
        response_data = {'answer': text,'studentid':id}
        # Serialize and save the response
        serializer = StudentResponseSerializer(data=response_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to save response'}, status=status.HTTP_400_BAD_REQUEST)

    except sr.UnknownValueError:
        return Response({'error': 'Speech recognition could not understand audio'}, status=status.HTTP_400_BAD_REQUEST)
    except sr.RequestError as e:
        return Response({'error': f'Speech recognition request error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@student_required
def saveResponse(request):
        transcript = request.data.get('transcript')
        questionId = request.data.get('questionId')
        student_instance = request.user
        if not student_instance:
           return Response({'error': 'Student DoesNot exist'})
       
        testAlreadyTaken=ModelResponse.objects.filter(studentid=student_instance.id).first()
        if not testAlreadyTaken:
            existing_response = StudentResponses.objects.filter(
            studentid=student_instance.id,
            questionnaire=questionId).first()
        # If an existing response is found, update it
            if existing_response:
                existing_response.answer = transcript
                existing_response.submitted = True
                existing_response.save()
                serializer = StudentResponseSerializer(existing_response)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # Create a dictionary with the recognized text
            response_data = {'answer': transcript, 'studentid': student_instance.id,'submitted': True,'questionnaire':questionId}
            # Serialize and save the response
            serializer = StudentResponseSerializer(data=response_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            existing_response = StudentResponses.objects.filter(
            studentid=student_instance.id,
            testType='test2',
            questionnaire=questionId).first()
            
            if existing_response:
                existing_response.answer = transcript
                existing_response.submitted = True
                existing_response.save()
                serializer = StudentResponseSerializer(existing_response)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # Create a dictionary with the recognized text
            response_data = {'answer': transcript, 'studentid': student_instance.id,'submitted': True,'questionnaire':questionId,'testType':'test2'}
            # Serialize and save the response
            serializer = StudentResponseSerializer(data=response_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def saveResponseId(request,id):
        
        transcript = request.data.get('transcript')
        print(1)
        student_instance = User.objects.get(id=id)
        if not student_instance:
           return Response({'error': 'Student DoesNot exist'})
        # Create a dictionary with the recognized text
        print(2)
        response_data = {'answer': transcript, 'studentid': id}
        # Serialize and save the response
        serializer = StudentResponseSerializer(data=response_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def updateResponse(request, id):
     transcript = request.data.get('transcript')
     response_data = StudentResponses.objects.get(id=id, studentid=request.user.id)
     if not response_data:
           return Response({'error': 'Response Does Not exist'})
        # Create a dictionary with the recognized text
        
     response_data.answer=transcript
        # Serialize and save the response
     serializer = StudentResponseSerializer(data=response_data)
     if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['DELETE']) 
# def delete(request,id):
#         questionnaire = get_object_or_404(Questionnaire, pk=id)
#         questionnaire.delete()
#         return Response({'message': 'Questionnaire deleted successfully'})
    
# @api_view(['PUT']) 
# def updateQuestionaire(request,id):

#         questionnaire = get_object_or_404(Questionnaire, pk=id)
#         if not questionnaire:
#          return Response({'message': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)
       
#         updatedQuestionaire=QuestionSerializer(questionnaire,data=request.data)
       
#         if updatedQuestionaire.is_valid():
#            updatedQuestionaire.save()
#            return Response({'message':'Questionaire updated'})
#         return Response({'message': 'Questionnaire Failed to update'})
  