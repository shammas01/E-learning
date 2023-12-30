from django.shortcuts import get_object_or_404, render
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
        if (user is not None) and user.is_admin is True:
            login(request, user)
            return redirect('admin_home')
            # return JsonResponse(
            #     data={
            #         'success': 'Logged in successfully',
            #         'redirect': redirect('admin_home')
            #     }
            # )
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






@superuser_login_required(login_url='admin_login')
def Admin_User_listing(request):
    # users = User.objects.filter(is_admin=True).order_by('-date_joined')
    users = User.objects.all().order_by('-date_joined')
    data = {'users': users}
    return render(request, 'admin_user.html', context=data)


@superuser_login_required(login_url='admin_login')
def User_profile(request, pk):
    user = get_object_or_404(User.objects, id=pk)
    
    data = {
        'user': user,
        
        
    }
    return render(
        request=request,
        template_name='admin_profile_page.html',
        context=data,
    )




@superuser_login_required(login_url='admin_login')
def Admin_tutor_listing(request):
    tutors = TutorModel.objects.all()
    aptutors = TutorModel.objects.filter(approved=True)
    notaptutors = TutorModel.objects.filter(approved=False)

    data = {'tutors':tutors,'aptutors':aptutors,'notaptutors':notaptutors}
    
    return render(request, 'admin_tutors.html',context=data)



def Tutor_Profile(request,pk):
    tutor = get_object_or_404(TutorModel.objects, id=pk)
    data = {
        'tutor': tutor,
    }
    if tutor.approved == False:
        return render(
                      request=request,
                      template_name="tutor_update.html",
                      context=data
                      )
    else:
        return render(
            request=request,
            template_name='admin_tutor_profile.html',
            context=data,
        )


def tutorapprovel(request):
    pass