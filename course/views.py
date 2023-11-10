from django.http import Http404
from . models import (
            CategoryModel,
            CourseContentModel,
            CourseDetailsModel,
            CourseRatingModel,
            LiveClassContentsModel,
            LiveClassDetailsModel)
from . serializers import CourseDetailsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tutor.models import TutorModel
from rest_framework import status
# Create your views here.


class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = CourseDetailsModel.objects.get(tutor=request.user.tutormodel)    
        serializer= CourseDetailsSerializer(data)
        return Response(serializer.data)


    def post(self, request):
        serializer = CourseDetailsSerializer(data=request.data)
        
        try:
            tutor = TutorModel.objects.get(user=request.user)
            print(tutor)
        except TutorModel.DoesNotExist:
            raise Http404("Tutor not found.")
        
        if tutor.approved is True and tutor.is_block is False:
            if serializer.is_valid():
                course = CourseDetailsModel.objects.create(
                    tutor = tutor,
                    heading = serializer.validated_data.get('heading'),
                    contents = serializer.validated_data.get('contents'),
                    description = serializer.validated_data.get('description'),
                    duration = serializer.validated_data.get('duration'),
                    language = serializer.validated_data.get('language'),
                    catogory = serializer.validated_data.get('catogory')
                )
                response = {"messege":"courser detail are created",
                            "data":serializer.data}
                return Response(response,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"messege":"somthing wrong!!.. contact admin"})


    def put(self, request):
        course_details = CourseDetailsModel.objects.get(tutor=request.user.tutormodel)   
        serializer = CourseDetailsSerializer(course_details,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'messge':"updated successfully","data":serializer.data})
        return Response(serializer.errors)