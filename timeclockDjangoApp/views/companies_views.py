from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json



# shift routes
# @login_required
def company_index(request):

    # get user session
    loggedIn_user_id = request.session.get('user_id')

    if request.method == "GET":

        if not loggedIn_user_id:
            with connection.cursor as cursor:
                cursor.execute('SELECT * FROM shifts WHERE user_id = %s', [loggedIn_user_id])
                shifts = cursor.fetchall()

                 # Convert query results to a list of dictionaries
                shift_list = [{'id': row[0], 'shift_detail': row[1]} for row in shifts]
                
                return JsonResponse({'status': 'success', 'shifts': shift_list})
        else:
            return JsonResponse({'status': 'error', 'message': 'User ID not found in session'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def new_company(request, id):
    # return HttpResponse("shifts")
    if request.method == 'POST':
        user = request.session.get('user_id')

        data = json.loads(request.body)

        name = data.POST.get('name')
        start_time = data.POST.get('start_time', '').strip()
        end_time = data.POST.get('end_time', '').strip()
        pay_rate = data.POST.get('pay_rate', '').strip()
        start_date = data.POST.get('start_date', '').strip()

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S') 

        if not user:
            return JsonResponse({'status': 'error', 'message': 'User needs to login!'})
        
        try:
            if name and start_time and end_time and pay_rate and start_date:
                with connection.cursor() as cursor:
                    cursor.execute('''
                                INSERT INTO companies 
                                (user_id, name, start_time, end_time, pay_rate, start_date, created_on) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ''', [user, name, start_time, end_time, pay_rate, start_date, formatted_time])
                    if cursor.rowcount > 0:
                        return JsonResponse({'status': 'success', 'message': 'New Company Created Successfully!'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Something Went Wrong. Company Was Not Created Successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Field(s) is required'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message':str(e)})
    return JsonResponse({'status': 'error', 'message': 'Request Method Invalid'})

def company_details(request, id):
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
def updated_company(request, id):
    return HttpResponse("create a new shift")

def delete_company(request, id):
   return HttpResponse("delete shifts")