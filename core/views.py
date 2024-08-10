from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    return HttpResponse("Your server is working running succesfully")

def pendingpay(request):
    return render(request,'pendingpay.html')