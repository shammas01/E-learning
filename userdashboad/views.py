import random,math
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q , Prefetch
from course.models import CourseDetailsModel
from live.models import LiveClassDetailsModel
from . serializer import (TutorListserializer,
                          CourseListserializer,
                          TutorSelectSerializer,
                          CourseSelectSerializer,
                          LiveSelectSerializer,
                          UserProfileSerializer)
from rest_framework.response import Response
from rest_framework import status 
from tutor.models import TutorModel
from course.models import CourseDetailsModel
from . paginator import CustomUserListPagination
from live.models import LiveClassDetailsModel
from useraccount.authentication.smtp import send_email
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from useraccount.models import UserProfile
# Create your views here.



class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    @extend_schema(responses=UserProfileSerializer)
    def get(self, request):
        user = UserProfile.objects.get(
            user=request.user
        )  # we can create with 'get_or_create()' method.
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    serializer_class = UserProfileSerializer
    @extend_schema(responses=UserProfileSerializer)
    def put(self, request):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        email = request.data.get("user", {}).get("email")
        print(request.data)
        user_email = request.user.email
        print(user_email)
        if serializer.is_valid():
            if email and email != user_email:
                otp = math.floor((random.randint(100000, 999999)))
                subject = "Otp for account verification"
                message = f"Your otp for account verification {otp}"
                recipient_list = [email]
                send_email(subject=subject, message=message, email=recipient_list[0])
                request.session["email"] = email
                request.session["otp"] = otp
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseSearching(APIView):
    permission_classes = [AllowAny]

    serializer_class = CourseListserializer
    @extend_schema(responses=CourseListserializer)
    def get(self, reqeust):
        q = reqeust.GET.get("q")
        Q_base = Q()
        if q:
            Q_base = Q(heading__icontains=q) | Q(tutor__name__icontains=q)
        course = CourseDetailsModel.objects.filter(Q_base).select_related('tutor').prefetch_related("tutor__skills",'tutor__liveclassdetailsmodel_set')
        serializer = CourseListserializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class TutorListing(APIView):
    permission_classes=[AllowAny]

    serializer_class = UserProfileSerializer
    @extend_schema(responses=UserProfileSerializer)
    def get(self, request):
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
            return Response(serialzer.data)
        except Exception as e:
            return Response({"somthing wrong with your seralizer"})

        
    
        


class CourseListing(APIView):
    permission_classes = [AllowAny]

    sserializer_class = CourseSelectSerializer
    @extend_schema(responses=CourseSelectSerializer)
    def get(self, request):
        try:
            courses = CourseDetailsModel.objects.all()
        except CourseDetailsModel.DoesNotExist:
            raise Http404
            
        if courses:
            try:
                pagination = CustomUserListPagination()
                page_result = pagination.paginate_queryset(courses, request)
                serializer = CourseSelectSerializer(page_result, many=True)
                page_count = pagination.page.paginator.num_pages
                return Response({"data": serializer.data, "page_count": page_count})
            except Exception as e:
                print(e)
                return Response({"somting wrong with your serializer....."})
        return Response({"course not found"})
        


class LiveListing(APIView):
    permission_classes=[AllowAny]

    serializer_class = LiveSelectSerializer
    @extend_schema(responses=LiveSelectSerializer)
    def get(self,request):
        try:
            lives = LiveClassDetailsModel.objects.filter(
                session_status='Published'
            )

        except LiveClassDetailsModel.DoesNotExist:
            raise Http404("live not found")
        
        if lives:
            serializer = LiveSelectSerializer(lives,many=True)
            return Response(serializer.data)
        
        return Response({"somting wrong with your live serializer"})