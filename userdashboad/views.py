from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q , Prefetch
from course.models import CourseDetailsModel
from live.models import LiveClassDetailsModel
from . serializer import TutorListserializer,CourseListserializer,TutorSelectSerializer,CourseSelectSerializer
from rest_framework.response import Response
from rest_framework import status 
from tutor.models import TutorModel
from course.models import CourseDetailsModel
from . paginator import CustomUserListPagination

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
        Q_base = Q()
        if q:
            Q_base = Q(heading__icontains=q) | Q(tutor__name__icontains=q)
        course = CourseDetailsModel.objects.filter(Q_base).select_related('tutor').prefetch_related("tutor__skills",'tutor__liveclassdetailsmodel_set')
        serializer = CourseListserializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class TutorSlection(APIView):


    def get(self, request):
        live = request.GET.get('live')
        course = request.GET.get('course')
        tutor = request.GET.get('tutor')

        if tutor:
            result = self.get_tutor()
        if course:
            result = self.get_course()
            return Response(result,status=status.HTTP_200_OK)
        return Response(result,status=status.HTTP_400_BAD_REQUEST)

        
    def get_tutor(self):
        try:
            tutors = TutorModel.objects.filter(
                Q(approved=True),
                Q(is_block = False)
                )
            if not tutors.exists():
                print('tutor not found')
        except TutorModel.DoesNotExist:
            print('data not found')
        try:
            serialzer = TutorSelectSerializer(tutors,many=True)
            return serialzer.data
        except Exception as e:
            return {"somthing wrong with your seralizer"}
    

    def get_course(self):
        try:
            courses = CourseDetailsModel.objects.all()
        except CourseDetailsModel.DoesNotExist:
            raise Http404
        
        if courses:
            serializer = CourseSelectSerializer(courses, many=True)
            return serializer.data
        return {"somting wrong with your serializer"}

        
