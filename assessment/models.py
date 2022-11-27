from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser


USER_TYPE = (
    ("Student", "Student"),
    ("Teacher", "Teacher")
)

class User(AbstractBaseUser):
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100,null=False)
    email = models.EmailField(unique=True,db_index=True,null=False)
    profile_photo = models.FileField(null=False,upload_to="profile_pic/")
    user_type = models.CharField(max_length=10,choices = USER_TYPE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return str(self.email)

    #for user token 
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class User_Device_Detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255)
    user_access_token = models.CharField(max_length=255)

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50,null=False)
    date_time=models.IntegerField(null=False)
    created_by= models.CharField(max_length=50,null=False)

class Question_Answer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    question = models.TextField(null=False)
    answer=models.TextField(null=False)

    def __str__(self) -> str:
        return self.assessment.subject_name

class Student_Answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer, on_delete=models.CASCADE, related_name='question_answer_id', null=False)
    answer = models.TextField(null=False)

    def __str__(self) -> str:
        return self.user