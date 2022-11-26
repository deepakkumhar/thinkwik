from django.http import JsonResponse

def error_400(request, message):
    response = JsonResponse(data={'message': message})
    response.status_code = 400
    return response

def error_404(request, message):
    response = JsonResponse(data={'message': message})
    response.status_code = 404
    return response