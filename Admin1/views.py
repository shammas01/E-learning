from django.shortcuts import render
from rest_framework.views import APIView
from live.models import LiveClassDetailsModel
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.urls import reverse

# Create your views here.

class LiveListView(APIView):
    def get(self, request):
        pass


class AdminLoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin_home')
    
    def post(self, request):
        email = request.POST['email']
        password = request.POSt['password']

        user = authenticate(request, email=email, password=password)

        if user and user.is_superuser:
            login(request, user)
            return JsonResponse(
               data = {
                   
                   'sucsses':'longgind successfully',
                   'redirect':reverse('admin_home')

                
                }
            )