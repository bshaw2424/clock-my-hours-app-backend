from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# shift routes
@login_required
def shift_index(request):

    # get user session
    loggedIn_user_id = request.session.get('user_id')

    if request.method == "GET":

        if loggedIn_user_id is not None:
            with connection.cursor as cursor:
                cursor.execute('SELECT * FROM shifts WHERE user_id = %s', [loggedIn_user_id])
                shifts = cursor.fetchall()

                 # Convert query results to a list of dictionaries
                shift_list = [{'id': row[0], 'shift_detail': row[1]} for row in shifts]
                
                return JsonResponse({'status': 'success', 'shifts': shift_list})
        else:
            return JsonResponse({'status': 'error', 'message': 'User ID not found in session'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def shift_details(request, id):
    return HttpResponse("shifts")

def update_shift(request, id):
   # return HttpResponse("shifts")
    data = json.loads()
    if request.method == "GET":
        time = data.get("start_time")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE shifts SET start_time, end_time, shift_type, lunch_time, total_hours, notes, date WHERE id = %s", 
        [id])
        shift = cursor.fetchone()

    if shift:
        return JsonResponse({'status': 'success', 'message': 'update successful'})
    return JsonResponse({'status': 'error', 'message': 'update failed'}, status=400)

# create new shift
def new_shift(request):
    return HttpResponse("create a new shift")

def delete_shift(request, id):
   return HttpResponse("delete shifts")