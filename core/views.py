from django.http import HttpResponse
def index(request):
    return HttpResponse("Your server is working running succesfully")