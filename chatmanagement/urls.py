from django.urls import path
from chatmanagement import views
from django.contrib import admin 
from django.urls import path, include

urlpatterns = [  
    path('getChatUsers/',views.getChatUsersWithSpecificGroups),
    path('sendMessage/<int:id>/',views.sendMessage),
    path('getMessages/<int:id>/',views.getMessages),
    path('deleteMessage/<int:id>/',views.deleteMessages),
    path('updateProfile/',views.updateProfile),
    path('getProfile/',views.getProfile),
]


