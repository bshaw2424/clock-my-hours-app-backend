"""
URL configuration for timeclockDjangoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index_views, shift_views, timeoff_views, user_views, companies_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Index URLs
    path('', index_views.index, name='index'),
    path('login/', index_views.login_view, name='login'),
    path('register/', index_views.register, name='register'),
    path('logout/', index_views.logout_view, name='logout'),
    
    # Companies URLs
    path('companies/', companies_views.company_index, name='company_index'),
    path('companies/new', companies_views.new_company, name='new_company'),
    path('companies/<int:id>/', companies_views.company_details, name='company_details'),
    path('companies/<int:id>/update/', companies_views.update_company, name='update_company'),
    path('companies/<int:id>/delete/', companies_views.delete_company, name='delete_company'),

    # Shift URLs
    path('shift/', shift_views.shift_index, name='shift_index'),
    path('shift/new/', shift_views.new_shift, name='new_shift'),
    path('shift/<int:id>/', shift_views.shift_details, name='shift_details'),
    path('shift/<int:id>/update/', shift_views.update_shift, name='update_shift'),
    path('shift/<int:id>/delete/', shift_views.delete_shift, name='delete_shift'),
    
    # Timeoff URLs
    path('timeoff/', timeoff_views.timeoff_index, name='timeoff_index'),
    path('timeoff/new/', timeoff_views.new_timeoff, name='new_timeoff'),
    path('timeoff/<int:id>/', timeoff_views.timeoff_details, name='timeoff_details'),
    path('timeoff/<int:id>/update/', timeoff_views.update_timeoff, name='update_timeoff'),
    path('timeoff/<int:id>/delete/', timeoff_views.delete_timeoff, name='delete_timeoff'),
    
    # User URLs
    path('user/', user_views.user_index, name='user_index'),
    path('user/<int:id>/', user_views.user_details, name='user_details'),
    path('user/<int:id>/update/', user_views.user_update, name='user_update'),
    path('user/<int:id>/delete/', user_views.user_delete, name='user_delete'),
]