from django.http import JsonResponse


def handler404(request,exception):
    message = ('Route Not Found')
    response = JsonResponse(data={'error':message})
    response.status_code = 404
    return response

def handler500(request):
    message = ('Inter Server Problem')
    response = JsonResponse(data={'error':message})
    response.status_code = 500
    return response


