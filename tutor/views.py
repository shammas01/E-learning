from django.shortcuts import render
from rest_framework.views import APIView
from useraccount.models import User
from rest_framework import status
from . models import SkillModel,TutorModel
from . serializers import TutorSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from useraccount.authentication.smtp import send_email
from useraccount.authentication.twilio import send_phone_sms,phone_otp_verify
# Create your views here.


class TutorRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=TutorModel.objects.get(user=request.user)
        serializer = TutorSerializer(user)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tutor = TutorModel(
                user = request.user,
                profile_picture=serializer.validated_data.get('profile_picture'),
                resume=serializer.validated_data.get('resume'),
                phone=serializer.validated_data.get('phone')
            )
            tutor.save()

            skills = serializer.validated_data.get('skills')
            tutor.skills.set(skills)
            print(tutor.phone)
            verification_sid = send_phone_sms(tutor.phone)
            
            return Response({"verification_sid": verification_sid,"data":serializer.data,"message": "Your credentials are saved"})
        return Response({"msg": "Wrong", "errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)