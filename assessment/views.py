from .serializer import *
from .models import *
from .utils import *

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters

import datetime


# reister api.
class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                print(error_msg_value)
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))

        return Response({"message": "You are successfully Register",
                         "data": {
                                 'username': data['user'].username,
                                 'email': data['user'].email,
                                 'user_type': data['user'].user_type,
                                 'profile_photo': str(data['user'].profile_photo.path)},
                             'access_token': data['token']

                         })


#login api
class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            print(request.POST)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))

        return Response({"message": "You are successfully Login",
                         "data": {
                                 'username': data['user'].username,
                                 'email': data['user'].email,
                                 'user_type': data['user'].user_type,
                                 'profile_photo': str(data['user'].profile_photo.path)},
                             'access_token': data['token']

                         })


#user profile api
class UserDetails(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    # parser_classes = (FormParser,)

    def get(self, request, *args, **kwargs):
        try:
            user_obj=User.objects.filter(id=request.user.id)
        except Exception as e:return error_404(request,message=str(e)) 
        user=user_obj[0]
        userprofile = {
            "message": "user details",
            "data": {
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'profile_photo': str(user.profile_photo.path)},     
        }
        return Response(userprofile)

#update user profile
class UserUpdate(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    
    # parser_classes = (FormParser,)

    def patch(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': self.request.user})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))
        return Response({'message':'user profile update successfuly'})

#change password api
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': request.user})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))
        return Response({'message':'password updated successfuly'})
        
#user logout
class LogoutView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        data=(request.headers)
        tokens = list(data['Authorization'].split(" "))[1]
        User_Device_Detail.objects.filter(user=request.user,user_access_token=tokens).delete()
        return Response({'message':'logout successfuly'})

#add assessment api
class AddAssessment(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddAssessmentSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': request.user})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))

        return Response({"message": "assessment add successfuly"})

#list of assessment api
class ListAssessment(generics.ListAPIView):
    serializer_class=ListAssessmentSerializer
    queryset = Assessment.objects.all()
    search_fields = ['subject_name']
    filter_backends = [ filters.SearchFilter]
    # filterset_fields = ["is_discontinued",]
    search_fields = ["subject_name"]

    paginate_by = 5
    def get_queryset(self):
        return super().get_queryset()
    

#assessment details api
class DetailsAssessment(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id,*args, **kwargs):
        list_question_answer=[]
        question_answer_obj=Question_Answer.objects.filter(assessment=id)
        if not question_answer_obj.exists():
            return error_400(request,message="given id not found")
        for question_answer in Question_Answer.objects.filter(assessment=id):
            question_answer_dic={}
            question_answer_dic={
                "id":question_answer.id,
                "question":question_answer.question,
            }
            if User.objects.filter(id=request.user.id)[0].user_type=="Teacher":
                question_answer_dic["answer"]=question_answer.answer
            list_question_answer.append(question_answer_dic)

        return Response({
        "message": "assessment details",
        "data":{
        "subject_name":question_answer_obj[0].assessment.subject_name,
        "date_time":datetime.datetime.fromtimestamp(question_answer_obj[0].assessment.date_time),
        "created_by":question_answer_obj[0].assessment.created_by,
        "list": list_question_answer}
        })

#student answer api 

class AnswerAssessment(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerAssessmentSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': request.user})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))

        return Response({"message": "assessment answer add successfuly"})

#delete assessment api

class DeleteAssessment(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        if User.objects.filter(id=request.user.id)[0].user_type=="Student":
            return error_400(request,message="you are not authorized person")
        assessment_obj=Assessment.objects.filter(id=id)
        if not assessment_obj.exists():
            return error_400(request,message="given assessment id not exist")
        assessment_obj.delete()

        return Response({"message": "assessment delete successfuly"})
    
#edit assessment api
class EditAssessment(generics.GenericAPIView):
    serializer_class = EditAssessmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,context={'user': request.user,'assessment_id':id})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:return error_400(request,message=str(e))
        return Response({'message':'assessment update successfuly'})
