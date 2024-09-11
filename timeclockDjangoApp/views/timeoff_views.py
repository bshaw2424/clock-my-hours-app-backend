from django.http import HttpResponse
from django.shortcuts import render

# timeoff views
def timeoff_index(request):
    return HttpResponse("timeoff")

def new_timeoff(request):
    return HttpResponse("timeoff creating new form")

def timeoff_details(request, id):
    return HttpResponse("timeoff details")

def update_timeoff(request, id):
    return HttpResponse("timeoff update")

def delete_timeoff(request, id):
    return HttpResponse("timeoff delete")
