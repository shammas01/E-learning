from django.shortcuts import render
from rest_framework.views import APIView
from useraccount.models import User
from rest_framework import status
from . models import SkillModel,TutorModel
from . serializers import TutorSerializer,TutorUpdateSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from useraccount.authentication.smtp import send_email_for_tutor
from useraccount.authentication.twilio import send_phone_sms,phone_otp_verify
from useraccount.serializers import OtpSerializer,PhoneOtpSerializer

# Create your views here.


class TutorRrgistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TutorSerializer(data=request.data)
        try:
            data = TutorModel.objects.get(user = request.user)
            print(data)
            return Response({"messge":"user data is already exist"})
        except TutorModel.DoesNotExist:
            if serializer.is_valid(raise_exception=True):
                tutor = TutorModel(
                    user = request.user,
                    profile_picture=serializer.validated_data.get('profile_picture'),
                    resume=serializer.validated_data.get('resume'),
                    
                )
                tutor.save()
                subject='Registration For Tutor'
                messege = 'Congragulation your application has been saved. We will contact you'
                send_email_for_tutor(subject=subject, message=messege, email=tutor.user)

                skills = serializer.validated_data.get('skills')
                tutor.skills.set(skills)
                
                response = {"messege":"your registration prosses are commpleted",
                            "data":serializer.data}
                return Response(response,status=status.HTTP_200_OK)
        return Response({"msg": "Wrong", "errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        user = TutorModel.objects.get(user=request.user)
        if user.is_block is False:
            if user.approved is True:
                serializer =  TutorSerializer(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"messege":"your application still pending. we will contact you"})
        return Response({"messege":"you are blocked. contact with admin"})
    

    def put(self, request):
        tutor_profile = request.user.tutormodel
        print(tutor_profile)
        serializer = TutorUpdateSerializer(tutor_profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class TutorPhoneVerification(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = PhoneOtpSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone_number')
            request.session['phone'] = phone
            try:
                verification_sid = send_phone_sms(phone)
                request.session['sid'] = verification_sid
                return Response({"sid":verification_sid},status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
            return Response({"messege":"somting was wrong with your phone verification"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class PhoneOtpVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            verification_sid = request.session.get('sid')
            print(verification_sid)
            try:
                verification_check = phone_otp_verify(verification_sid,otp)
                print(verification_check.status) 
            except:
                return Response({"messege":"somthing was wrong"})
            if verification_check.status == 'approved':
                phone_number = request.session.get('phone')
                tutor_profile = TutorModel.objects.get(user=request.user)
                tutor_profile.phone = phone_number
                tutor_profile.save()
                response_data = {
                    "msg":"your phone number is verifyed",
                }                                               
                return Response(response_data)
            return Response({'msg': 'Something Went Wrong...'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)