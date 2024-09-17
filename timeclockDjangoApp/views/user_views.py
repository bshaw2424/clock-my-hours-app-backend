from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# user index method
def user_index(request):
    if request.method == 'GET':
      
      # check for user session (logged in)
      loggedIn_user = request.session.get('user_id')

      if loggedIn_user:
         with connection.cursor() as cursor:
            cursor.execute('SELECT username, password, email FROM users WHERE id = %s', [loggedIn_user])
            found_user = cursor.fetchOne()
            if found_user:
                return JsonResponse({'status': 'success', 
                                     'username': found_user[0], 
                                     'password': found_user[1],
                                     'username': found_user[2]})
      else:
            return JsonResponse({'status': 'error', 'message': 'user not found!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request Method' }, status=400)

# show page method
def user_details(request, id ):
    if request.method == "GET":
        logged_in_user = request.session.get('user_id')

        if logged_in_user != id:
            return JsonResponse({'status': 'error', 'message': 'Permission Denied'})
        
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT username, password, email FROM users WHERE id = %s', [id])
                user = cursor.fetchone()
                if user:
                    return JsonResponse({
                        'status': 'success',
                        'username': user[0],
                        'password': user[1],
                        'email': user[2],
                    })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request Method'}, status=400)

# update method
def user_update(request, id):
    # return HttpResponse("user update")
    if request.method == "POST":

        data = json.loads()

        # user session
        update_user = request.session.get('user_id')

        email = data.POST.get('email', '').strip()
        password = data.POST.get('password', '').strip()
        username = data.POST.get('username', '').strip()

        # check if user is logged in
        if not update_user:
            return JsonResponse({'status': 'error', 'message': 'user not found'})

        # check if the session id is equal to user id
        if update_user != id:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'})
        
        # check if input fields are not empty then update
        if email and password and username:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('''UPDATE users 
                                   SET username = %s, password = %s, email = %s 
                                   WHERE id = %s''', 
                                   [username, password, email, id])
                return JsonResponse({'status': 'success', 'message': 'user details updated successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Inputs cannot be empty'})
    return JsonResponse({'status': 'error', 'message' : 'Invalid Request Method'}, status=400)

# delete method
def user_delete(request, id):
    if request.method == "POST":
        delete_user = request.session.get('user_id')

        if not delete_user:
           return JsonResponse({'status': 'error', 'message': 'user not found!'})
       
        if delete_user != id:
           return JsonResponse({'status': 'error', 'message': 'Permission Denied'})
       
        try:
            with connection.cursor() as cursor:
                # Execute the delete query
                cursor.execute('DELETE FROM users WHERE id = %s', [id])
                # Check if any row was deleted
                if cursor.rowcount == 0:
                    return JsonResponse({'status': 'error', 'message': 'User not found'})
            return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
       
           