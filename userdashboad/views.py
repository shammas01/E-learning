from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q , Prefetch
from course.models import CourseDetailsModel
from live.models import LiveClassDetailsModel
from . serializer import TutorListserializer,CourseListserializer
from rest_framework.response import Response
from rest_framework import status   

# Create your views here.


class CourceListForUser(APIView):
    def get(self , request):
        q = request.GET.get("q")
        course = request.GET.get("course")
        tutor = request.GET.get("tutor")




class CourseSearching(APIView):
    permission_classes = [AllowAny]
    def get(self, reqeust):
        q = reqeust.GET.get("q")
        Q_base = Q(heading__icontains=q) | Q(tutor__name__icontains=q)
        if not q:
            pass
        course = CourseDetailsModel.objects.filter(Q_base)
        serializer = CourseListserializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    