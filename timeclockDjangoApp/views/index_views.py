from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from datetime import datetime
from django.contrib.auth.hashers import make_password
import json


# route to get csrftoken from react frontend
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


def index(request):
    return JsonResponse({'success': True, 'message': 'Hello World', 'correct': True}, status=200)


# login view
@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # load the data as json
        form_json_data = json.loads(request.body)
        email = form_json_data.get('email')
        password = form_json_data.get('password')

        authenticate_user = authenticate(request, username=email, password=password)

        # authenticate user login
        if authenticate_user is not None:
            login(request, authenticate_user)

            # creates session for the user
            request.session['user_id'] = authenticate_user.id
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# register view
def register(request):

    username = request.POST.get('username') 
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm')
    
    # compare password and confirmed password inputs
    if password != confirm_password:
        return JsonResponse({'error': 'passwords do not match. Please try again!'}, status=400)
    
    hashed_password_registered = make_password(password)

    try:
        with connection.cursor() as cursor:

            # get the time and format it to insert in the database
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s)',
            [username, email, hashed_password_registered, formatted_time])
            
            user_created = cursor.fetchone()[0]
        
        return JsonResponse({'message': 'Form submitted successfully', 'user': user_created})
    
    except Exception as error:
        
        return JsonResponse({'error': str(error)}, status=500)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)