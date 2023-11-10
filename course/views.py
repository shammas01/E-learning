from django.http import Http404
from . models import (
            CategoryModel,
            CourseContentModel,
            CourseDetailsModel,
            CourseRatingModel,
            LiveClassContentsModel,
            LiveClassDetailsModel)
from . serializers import CourseDetailsSerializer,CourseContentSerializer,CourseDetailsListCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tutor.models import TutorModel
from rest_framework import status
from rest_framework import viewsets
# custom permissions....
from . permissions import IsTutorOrReadOnly
# Create your views here.


class ListCreateCourseView(APIView):
    permission_classes = [IsAuthenticated,IsTutorOrReadOnly]
    def get(self, request):
        data = CourseDetailsModel.objects.filter(tutor=request.user.tutormodel)
        serializer= CourseDetailsListCreateSerializer(data,many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CourseDetailsListCreateSerializer(data=request.data)
        
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



class RetriveUpdateDistroyView(APIView):
    permission_classes = [IsAuthenticated,IsTutorOrReadOnly]
    
    def get_object(self, pk):
        try:
            return CourseDetailsModel.objects.get(id=pk, tutor=self.request.user.tutormodel)
        except CourseDetailsModel.DoesNotExist:
            raise Http404
        

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDetailsSerializer(course)
        return Response(serializer.data)
    

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDetailsSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"messege":"your data updated","data":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response({"messege":"your course removed"},status=status.HTTP_204_NO_CONTENT)



