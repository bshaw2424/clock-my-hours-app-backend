from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# timeoff views
def timeoff_index(request):
    # return HttpResponse("timeoff")
    if request.method == 'GET':
        user = request.session.get('user_id')

        if not user:
            return JsonResponse({'status': 'error', 'message': 'Permission Denied'})
        
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT vacation_hours, sick_hours, dayoff_type FROM time_off WHERE id = %s', [user])
                time_off_data = cursor.fetchall()

                if time_off_data:
                    time_off_data([
                        {
                        'vacation_hours': row[0], 
                        'sick_hours': row[1], 
                        'dayoff_type': row[2]
                        } 
                        for row in time_off_data
                    ])
                    return JsonResponse({'status': 'success', 'data': time_off_data})
                else:
                    return JsonResponse({'status': 'error', 'message': 'No Time Off Data!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
    return JsonResponse({'status': 'error', 'message': 'Request Method Invalid'})

# insert new time route
def new_timeoff(request):
    # return HttpResponse("timeoff creating new form")
    if request.method == 'POST':
        user = request.session.get('user_id')

        data = json.loads(request.body)

        vacation_hours = data.get('vacation_hours', '').strip()
        sick_hours = data.get('sick_hours', '').strip()
        dayoff_type = data.get('dayoff_type', '').strip()

        # check if user is logged in
        if not user:
            return JsonResponse({'status': 'error', 'message': 'Permission Denied'})
        
        # query the company table to get the company_id for user add a record
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM company WHERE user_id = %s', [user])
            get_company_userId = cursor.fetchall()

            if get_company_userId:
                 for company_id_tuple in get_company_userId:
                    company_id = company_id_tuple[0]
                        

        try:
            if vacation_hours and sick_hours and dayoff_type:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO time_off (vacation_hours, sick_hours, dayoff_type, user_id, company_id) VALUES (%s, %s, %s, %s, %s)", 
                    [vacation_hours, sick_hours, dayoff_type, user, company_id])
                if cursor.rowcount > 0:
                    return JsonResponse({'status': 'success', 'message': 'Time Off Created Successfully!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Something Went Wrong. Time Off Not Successfully Created!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'All Fields are Required'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Request Method Invalid'})
        

def timeoff_details(request, id):
    return HttpResponse("timeoff details")

def update_timeoff(request, id):
    return HttpResponse("timeoff update")

def delete_timeoff(request, id):
    return HttpResponse("timeoff delete")
