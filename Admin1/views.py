from django.shortcuts import render
from rest_framework.views import APIView
from live.models import LiveClassDetailsModel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from rest_framework.response import Response
from django.urls import reverse
from rest_framework import status
from . helper import superuser_login_required
# Create your views here.

    

def admin_login(request):
    # if request.user.is_authenticated and request.user.is_admin:
    #     return redirect('admin_home')
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response
        
        user = authenticate(request, username=username, password=password)
        if (user is not None) and user.is_admin:
            login(request, user)
            return JsonResponse(
                data={
                    'success': 'Logged in successfully',
                    # 'redirect': reverse('admin_home')
                }
            )
        else:
            response = JsonResponse(
                data={
                    'error': 'Invalid username or password'
                }
            )
            response.status_code = 400
            return response
    return render(request, 'admin_login.html')



@superuser_login_required(login_url='admin_login')
def admin_home(request):
    analytics = [
        {
            'title': 'No. of Users',
            'value': User.admin_objects.all().count()
        },
        # {
        #     'title': 'No. of Posts',
        #     'value': Post.admin_objects.all().count()
        # },
        # {
        #     'title': 'No. of Reports',
        #     'value': Report.objects.all().count()
        # },
        
        # {
        #     'title': 'No. of Comments',
        #     'value': Comment.admin_objects.all().count()
        # }
    ]
    data = {
        'analytics': analytics
    }
    return render(request, 'admin-home.html', context=data)