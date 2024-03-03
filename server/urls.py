from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path, include


urlpatterns = [  
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('signup/',views.signup),
    path('logout/',views.logout),
    path('getUsers/',views.get_all_users),
    path('forgot_password/',views.forgetPassword),
    path('change_password/',views.changePassword),
    path('deleteUser/<int:id>/',views.delete_user_by_id),
    path('question/',include('questionaire.urls')),
    path('response/',include('responsemanagement.urls')),  
    path('chat/',include('chatmanagement.urls')),
]


