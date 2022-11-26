from rest_framework_simplejwt.tokens import AccessToken
from .utils import *
from .models import *
# url=['/user-details/']
def token_check(get_response):
    def middleware(request):
        if 'Authorization' in request.headers:
        # if request.path in url:
            data=(request.headers)
            try:
                tokens = list(data['Authorization'].split(" "))[1]
                access_token_obj = AccessToken(tokens)
            except:
                return error_400(request,message="Invalid Token. You are not authenticated to access this endpoint")
            user_id=access_token_obj['user_id']
            if not User_Device_Detail.objects.filter(user=user_id).filter(user_access_token=tokens).exists():
                return error_400(request, message='you are not login')
        response = get_response(request)
        return response  

    return middleware