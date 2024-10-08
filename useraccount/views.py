from django.http import Http404
from rest_framework.views import APIView
from .models import User
from .serializers import (
    Emailsmtpserializer,
    OtpSerializer,
    GoogleSocialAuthSerializer,
    UserRegisterSerializer,
    LoginSerializer
)
import math, random
from useraccount.authentication.smtp import send_email
from useraccount.authentication.jwt import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

# Create your views here.


class Register(APIView): #for sample (03-10-24)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')


            otp = math.floor((random.randint(10000,99999)))

            subject = "Otp verivication"
            messege = f"verify with this otp {otp}"
            resipt = [email]
            sendmail = send_email(subject=subject, message=messege, email = resipt[0])
            print(">>>>>>>>>>>>>>.",sendmail)
            request.session["email"] = email
            request.session['otp'] = otp

            user = User.objects.create(
                email = email,
                password = password,
                username = username
            )

            return Response(
                {"email":email, "message":" registration is completed, veryfiy your account"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )






class RegisterEmailSendView(APIView):
    permission_classes_classes = [AllowAny]
    
    serializer_class = UserRegisterSerializer
    @extend_schema(responses=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            

            User.objects.create_user(
                email = email,
                password = password,
                username = username
            )

            otp = math.floor((random.randint(100000, 999999)))
            print(otp)
            subject = "Otp for account verification"
            message = f"Your otp for account verification {otp}"
            # email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject=subject, message=message, email=recipient_list[0])
            request.session["email"] = email
            request.session["otp"] = otp
            request.session['password'] = password
            return Response(
                {"email": email, "messegte": "email send successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmailVerify(APIView):

    serializer_class = OtpSerializer
    @extend_schema(responses=OtpSerializer)
    def post(self, request):
        otp = request.data.get('otp')
        saved_otp = request.session.get('otp')
        email = request.session.get('email')
        
        print('otp=',otp,'saved otp=',saved_otp)
        if otp == saved_otp:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise Http404('user not found')
            user.is_active = True
            user.save()
            
            return Response("you account successfull activated")
        
        return Response("invalid otp")



class loginView(APIView):

    serializer_class = LoginSerializer
    @extend_schema(responses=LoginSerializer)
    def post(self, requset):
        serializer = LoginSerializer(data=requset.data)
    
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise Http404('user not found')

            if user.is_active == True:
                user1 = authenticate(email=email,password=password)
                token = get_tokens_for_user(user1)
                response = {
                    "Your email": email,
                    "token": token,
                    "messege": "your account successfull activated",
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response("verify you emeil otp then try to log..!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(APIView):

    serializer_class = GoogleSocialAuthSerializer
    @extend_schema(responses=GoogleSocialAuthSerializer)
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)



