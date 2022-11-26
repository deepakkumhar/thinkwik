"""thinkwik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from assessment.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('user-details/',UserDetails.as_view(),name="user-details"),
    path('user-update/',UserUpdate.as_view(),name="user-update"),
    path('change-password/',ChangePasswordView.as_view(),name="change-password"),
    path('logout/',LogoutView.as_view(),name="logout"),

    path('assessment-add/',AddAssessment.as_view(),name='add-assessment'),
    path('assessment-list/',ListAssessment.as_view(),name='list-assessment'),
    path('assessment-details/<int:id>/',DetailsAssessment.as_view(),name='details-assessment'),
    path('assessment-answer/',AnswerAssessment.as_view(),name='answer-assessment'),
    path('assessment-delete/<int:id>/',DeleteAssessment.as_view(),name='delete-assessment'),
    path('assessment-edit/<int:id>/',EditAssessment.as_view(),name='edit-assessment'),
    

]
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5NTQ1Nzg3LCJpYXQiOjE2Njk0NTkzODcsImp0aSI6ImNlNTk2NWE5NGIwOTQyOTliMTdiZjhhOGJiNmQ1MDRmIiwidXNlcl9pZCI6M30.uSayZHBUOqWFGeL5Ygn9SYjxPj9brYCocb_p6T0RNJw

#student
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5NTY4Mzg3LCJpYXQiOjE2Njk0ODE5ODcsImp0aSI6IjhmNWE3N2Q1YjNkMTRiMGI4ODk5YjYyMzdkM2YyMjAzIiwidXNlcl9pZCI6OH0.sqK8a638_-YgnmDBjKrtd7PupJ1pAE-TBdqOnCh84lo

#teacher
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5NTcxOTE2LCJpYXQiOjE2Njk0ODU1MTYsImp0aSI6ImM3N2Q5MGM5YzY1NzQ4MzFiZmVjMWY5NDY3MGY3Y2YyIiwidXNlcl9pZCI6OX0.s5W7bFchc_7_6xjwwTXwe1Q_LLdLkPijvBQkg1prJqg