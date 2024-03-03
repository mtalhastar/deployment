from django.urls import path
from responsemanagement import views
from django.contrib import admin 
from django.urls import path, include

urlpatterns = [  
    path('speechToText/<int:id>/',views.saveStudentResponse),
    path('savemessage/',views.saveResponse),
    # path('savemessage/<int:id>/',views.saveResponseId),
    path('getmessageofAstudent/',views.getAStudentResponse),
    path('getmessage/',views.getAllStudentResponses),
    path('deletemessage/',views.deleteAllStudentResponses),
    path('getAIResponses/',views.getAllAIResponses),
    path('deleteresponse/<int:id>/',views.deleteSpecificResponse),
    path('filter/',views.filteredStudents),
    path('testSubmission/',views.testIfResponseSubmitted),
]



    
