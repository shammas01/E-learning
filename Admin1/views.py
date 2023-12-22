from django.shortcuts import render
from rest_framework.views import APIView
from live.models import LiveClassDetailsModel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse, HttpRequest
from rest_framework.response import Response
from django.urls import reverse
from rest_framework import status
from . helper import superuser_login_required
from useraccount.models import User
from tutor.models import TutorModel
from course.models import CourseDetailsModel
from live.models import LiveClassDetailsModel
# Create your views here.

    

def admin_login(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_home')
    
    if request.method == 'POST':
        try:
            email = request.POST['username']
            password = request.POST['password']
            
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response
        print(f"Received username: {email}, password: {password}")

        user = authenticate(email=email, password=password)

        
        
        print(user)
        if (user is not None) and user.is_admin:
            login(request, user)
            return JsonResponse(
                data={
                    'success': 'Logged in successfully',
                    'redirect': reverse('admin_home')
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
            'value': User.objects.all().count()
        },
        {
            'title': 'No. of Tutors',
            'value': TutorModel.objects.filter(approved=True).count()
        },
        {
            'title': 'No. of Course',
            'value': CourseDetailsModel.objects.all().count()
        },
        
        {
            'title': 'No. of Live sessinos',
            'value': LiveClassDetailsModel.objects.all().count()
        }
    ]
    data = {
        'analytics': analytics
    }
    return render(request, 'admin_home.html', context=data)


@superuser_login_required(login_url='admin_login')
def admin_logout(request: HttpRequest):
    logout(request)
    return redirect(
        to='admin_login'
    )