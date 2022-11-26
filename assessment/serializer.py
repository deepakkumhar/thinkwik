import random
from .models import *
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from django.contrib import auth
from rest_framework import serializers
import json
from django.db.models import Q


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message=("email id already exists"))])
    password = serializers.CharField(max_length=15, min_length=8, error_messages={'min_length': (
        'password should up to 8 character'), 'max_length': ('password length too much high')}, write_only=True)
    device_token = serializers.CharField(required=True)
    # profile_photo = serializers.ImageField(required=False)
    user_type =serializers.ChoiceField(choices=USER_TYPE)
    class Meta:
        model = User
        fields = ['email', 'password','username','user_type','profile_photo',
                  'device_token']

    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = u'email address cannot be blank'
        self.fields['email'].error_messages['required'] = u'email address is required'
        self.fields['password'].error_messages['required'] = u'password is required'
        self.fields['password'].error_messages['blank'] = u'password cannot be blank'
        self.fields['username'].error_messages['required'] = u'username is required'
        self.fields['username'].error_messages['blank'] = u'username cannot be blank'
        self.fields['profile_photo'].error_messages['required'] = u'profile_photo is required'
        self.fields['profile_photo'].error_messages['blank'] = u'profile_photo  cannot be blank'
        self.fields['user_type'].error_messages['required'] = u'user_type is required'
        self.fields['user_type'].error_messages['blank'] = u'user_type  cannot be blank'
        self.fields['device_token'].error_messages['required'] = u'device_token is required'
        self.fields['device_token'].error_messages['blank'] = u'device_token cannot be blank'

    def validate(self, data):
        try:
            validate_email(data['email'])
        except:
            raise serializers.ValidationError(
                "email must be valid email address")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        device_token = validated_data.pop('device_token')
        password = validated_data.pop('password')
        username_new = "".join(username.split(' ')).lower()
        if not User.objects.filter(username=username_new).exists():
            random_username = username_new
        else:
            random_username = username_new + str(random.randint(0, 1000))
        user = User.objects.create(
            username=random_username,
            **validated_data
        )
        user.set_password(password)
        user.save()
        user_access_token=user.tokens()['access']
        device=User_Device_Detail.objects.create(user=user,device_token=device_token,user_access_token=user_access_token)

        return {'user':user,'token':user_access_token}
        # return {'user': user, 'mobile': mobile_data}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    device_token = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['password'].error_messages['required'] = u'password is required'
        self.fields['password'].error_messages['blank'] = u'password cannot be blank'
        self.fields['username'].error_messages['required'] = u'username is required'
        self.fields['username'].error_messages['blank'] = u'username cannot be blank'
        self.fields['device_token'].error_messages['required'] = u'device_token is required'
        self.fields['device_token'].error_messages['blank'] = u'device_token cannot be blank'

    def validate(self, data):

        try:user_username = User.objects.get(
            Q(username=data['username']) | Q(email=data['username']))
        except:raise serializers.ValidationError("These credentials do not match our records")
        if not user_username.check_password(data['password']):
                raise serializers.ValidationError(
                    "These credentials do not match our records")
        return data

    def create(self, validated_data):
        user=User.objects.get(Q(email=validated_data['username']) | Q(username=validated_data['username']))
        user_access_token= user.tokens()['access']
        device_obj = User_Device_Detail.objects.filter(
            device_token=validated_data['device_token']).filter(user=user)
        if device_obj.exists():
            device_obj.update(user_access_token=user_access_token)
        else:
            User_Device_Detail.objects.create(user=user, user_access_token=user_access_token,
                                  device_token=validated_data['device_token'])
        
        return {'user':user,'token':user_access_token}

class UserUpdateSerializer(serializers.Serializer):
    email = serializers.CharField(required=False, validators=[UniqueValidator(
        queryset=User.objects.all(), message=("email id already exists"))])
    username=serializers.CharField(required=False)
    profile_photo=serializers.ImageField(required=False)
    def validate(self, data):
        try:
            validate_email(data['email'])
        except:
            raise serializers.ValidationError(
                "email must be valid email address")
        return data

    def create(self,validated_data):
        user=self.context.get("user")
        if validated_data.get('email') is not None:
            user.email=validated_data['email']
        if validated_data.get('username') is not None:
            user.email=validated_data['email']
            if not User.objects.filter(username=validated_data['username']).exists():
                random_username = validated_data['username']
            else:
                random_username = validated_data['username'] + str(random.randint(0, 1000))
            user.username=random_username
        if validated_data.get('profile_photo') is not None:
            user.profile_photo=validated_data['profile_photo']
        user.save()
        return True
        


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    new_password = serializers.CharField(max_length=15, min_length=8, error_messages={'min_length': (
        'password should up to 8 character'), 'max_length': ('password length too much high')}, write_only=True)
    class Meta:
        model = User
        fields=['password','new_password']
    def __init__(self, *args, **kwargs):
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)
        self.fields['password'].error_messages['blank'] = u'password cannot be blank'
        self.fields['password'].error_messages['required'] = u'password is required'
        self.fields['new_password'].error_messages['required'] = u'new_password is required'
        self.fields['new_password'].error_messages['blank'] = u'new_password cannot be blank'

    def validate(self, data):
        user=self.context.get("user")
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                "incorrect password ")
        return data

    def create(self, validated_data):
        user=self.context.get("user")
        user.set_password(validated_data['new_password'])
        user.save()
        return True


class AddAssessmentSerializer(serializers.ModelSerializer):
    question_answer=serializers.ListField(required=True)
    class Meta:
        model = Assessment
        fields=['subject_name','date_time','created_by','question_answer']
    def __init__(self, *args, **kwargs):
        super(AddAssessmentSerializer, self).__init__(*args, **kwargs)
        self.fields['subject_name'].error_messages['blank'] = u'subject_name cannot be blank'
        self.fields['subject_name'].error_messages['required'] = u'subject_name is required'
        self.fields['date_time'].error_messages['required'] = u'date_time is required'
        self.fields['date_time'].error_messages['blank'] = u'date_time cannot be blank'
        self.fields['created_by'].error_messages['required'] = u'created_by is required'
        self.fields['created_by'].error_messages['blank'] = u'created_by cannot be blank'
        self.fields['question_answer'].error_messages['required'] = u'question_answer is required'
        self.fields['question_answer'].error_messages['blank'] = u'question_answer cannot be blank'

    def validate(self, data):
        if User.objects.filter(id=self.context.get("user").id)[0].user_type=="Student":
            raise serializers.ValidationError("you are not authorized person")
        try:
            json.loads(data["question_answer"][0])
        except:
            raise serializers.ValidationError("please enter valid list of question and answer")
        return data

    def create(self, validated_data):
        date_time=int(validated_data.pop('date_time'))
        question_answers=validated_data.pop('question_answer')
        user=self.context.get("user")
        question_answers=json.loads(question_answers[0])
        assessment = Assessment.objects.create(user=user,date_time=date_time,**validated_data)
        for question_answer in question_answers:
            Question_Answer.objects.create(assessment=assessment,question=question_answer['question'],answer=question_answer['answer'])
        return True
    

class AnswerAssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student_Answer
        fields=['question','answer']

    def __init__(self, *args, **kwargs):
        super(AnswerAssessmentSerializer, self).__init__(*args, **kwargs)
        self.fields['question'].error_messages['blank'] = u'question cannot be blank'
        self.fields['question'].error_messages['required'] = u'question is required'
        self.fields['answer'].error_messages['required'] = u'answer is required'
        self.fields['answer'].error_messages['blank'] = u'answer cannot be blank'

    def validate(self, data):
        if self.context.get("user").user_type=="Teacher":
            raise serializers.ValidationError("you are not authorized person")
        return data

    def create(self, validated_data):
        Student_Answer.objects.create(user=self.context.get("user"),**validated_data)
        return True



class EditAssessmentSerializer(serializers.Serializer):
    subject_name=serializers.CharField(required=False)
    date_time=serializers.IntegerField(required=False)
    created_by=serializers.CharField(required=False)
    def validate(self, data):
        if self.context.get("user").user_type=="Student":
            raise serializers.ValidationError("you are not authorized person") 
        if not Assessment.objects.filter(id=self.context.get('assessment_id')).exists():
            raise serializers.ValidationError("given id not exist") 

        return data

    def create(self,validated_data):
        assessment=Assessment.objects.get(id=self.context.get('assessment_id'))
        if validated_data.get('subject_name') is not None:
            assessment.subject_name=validated_data['subject_name']
        if validated_data.get('date_time') is not None:
            assessment.date_time=validated_data['date_time']
        if validated_data.get('created_by') is not None:
            assessment.created_by=validated_data['created_by']
        assessment.save()
        return True

class ListAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ('id','subject_name', 'date_time','created_by')