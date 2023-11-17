from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from . serializers import ListLiveSerializer
from tutor.permissions import IsTutorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from . models import LiveClassDetailsModel
from tutor.models import TutorModel
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class LiveDetailListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTutorOrReadOnly]
    def post(self, request):
        serializer = ListLiveSerializer(data=request.data)
        try:
            teacher = TutorModel.objects.get(user=request.user)
        except TutorModel.DoesNotExist:
            raise Http404('teacher not found')
        
        if serializer.is_valid():
            if teacher.approved is True and teacher.is_block is False:
                live_details = LiveClassDetailsModel.objects.create(
                    teacher = teacher,
                    title = serializer.validated_data.get('title'),
                    description = serializer.validated_data.get('description'),
                    category = serializer.validated_data.get('category'),
                    day_duration = serializer.validated_data.get('day_duration'),
                    # session_type = serializer.validated_data.get('session_type'),
                    class_start_datetime = serializer.validated_data.get('class_start_datetime'),
                    class_duration = serializer.validated_data.get('class_duration'),
                    max_slots = serializer.validated_data.get('max_slots'),
                    pricing = serializer.validated_data.get('pricing'),
                    # session_status = serializer.validated_data.get('session_status'),
                    created_datetime = serializer.validated_data.get('created_datetime'),
                    last_updated_datetime = serializer.validated_data.get('last_updated_datetime')

                )
                response = {"message":"Live details successfull crated","data":serializer.data}
                return Response(response,status=status.HTTP_201_CREATED)
            return Response("somthing wrong with your account. contact admin")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)