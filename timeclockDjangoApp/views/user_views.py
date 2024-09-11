from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# user routes
def user_index(request):
    return HttpResponse("users")



def user_details(request, id):
    return HttpResponse("index details")

def user_update(request, id):
    return HttpResponse("index")

def user_delete(request, id):
   return HttpResponse("user delete")