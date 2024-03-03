from django.urls import path
from questionaire import views
from django.contrib import admin 
from django.urls import path, include

urlpatterns = [  
    path('getQuestionaire/',views.getQuestionaire),
    path('getStudentQuestionaire/',views.getStudentQuestions),
    path('createQuestionaire/',views.createQuestionaire),
    path('updateQuestionaire/<int:id>/',views.updateQuestionaire),
    path('removeQuestionaire/<int:id>/',views.delete),
    path('delete_all/',views.delete_all),
    path('update/',views.updatestatus)
]


