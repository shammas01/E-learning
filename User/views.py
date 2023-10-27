from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.configration.smtp import send_email
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import (IsAuthenticated,)
from django.conf import settings
import random,math
# Create your views here.










class EmailGetView(APIView):
    def post(self,request):
        serializer = EmailAuthViewSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = math.floor((random.randint(100000,999999)))
            subject = 'Otp for account verification'
            message = f'Your otp for account verification {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_email(subject, message, email_from, recipient_list)
            request.session['email'] = email
            request.session['otp'] = otp
            return Response({"email":email},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)