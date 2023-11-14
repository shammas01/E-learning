from django.http import Http404
from . models import (
            CategoryModel,
            CourseContentModel,
            CourseDetailsModel,
            CourseRatingModel,
            LiveClassContentsModel,
            LiveClassDetailsModel)
from . serializers import CourseDetailsSerializer,CourseContentSerializer,CourseDetailsListCreateSerializer,ContentPostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tutor.models import TutorModel
from rest_framework import status
from rest_framework import viewsets
# custom permissions....
from . permissions import IsTutorOrReadOnly
# Create your views here.




class ListCreateCourseDetailsView(APIView):
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



class RetriveUpdateCourseDetailsView(APIView):
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




class ListCreateCourseContentView(APIView):
    permission_classes = [IsAuthenticated,IsTutorOrReadOnly]
    
    def get(self, request,course_id):
        data = CourseContentModel.objects.filter(course_id=course_id)
        serializerv = CourseContentSerializer(data,many=True)
        return Response(serializerv.data)
    

    def post(self,request,course_id):
        try:
            tutor = TutorModel.objects.get(user=request.user)
            print(tutor)
        except TutorModel.DoesNotExist:
           return Response({"message": "Tutor not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            course = CourseDetailsModel.objects.get(tutor=tutor,id=course_id)
            print(course)
        except CourseDetailsModel.DoesNotExist:
            raise Http404("Course not found.")

        
        if tutor.approved is True and not tutor.is_block:
            serializer = ContentPostSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                print(serializer.data)
                CourseContentModel.objects.create(
                    course_id = course,
                    title = serializer.validated_data.get('title'),
                    description = serializer.validated_data.get('description'),
                    document = serializer.validated_data.get('document'),
                    video = serializer.validated_data.get('video'),
                    order = serializer.validated_data.get('order')
                )
                
                return Response({"messege":"your content succssesfully added","data":serializer.data})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response("somthing wrong...!!!")
