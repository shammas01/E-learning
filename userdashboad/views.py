import random,math
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q 
from course.models import CourseDetailsModel
from live.models import LiveClassDetailsModel
from . serializer import (
                          CourseSearchSerializer,
                          TutorListSerializer,
                          CourseListSerializer,
                          LiveListSerializer,
                          UserProfileSerializer,
                          TutorSelectSerializer,
                          CourseSelectSerializer,
                          LiveSelectSerializer,
                          UserCartSerializer,
                          CartItemSerializer)
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
from useraccount.serializers import OtpSerializer,PhoneOtpSerializer
from rest_framework.decorators import permission_classes
from useraccount.authentication.twilio import send_phone_sms,phone_otp_verify
from . models import UserCart,CartItem

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


@permission_classes([IsAuthenticated])
class EmailUpdatdOtpView(APIView):
    serializer_class = OtpSerializer

    @extend_schema(responses=OtpSerializer)
    def post(self, request):
        serialize = OtpSerializer(data=request.data)
        if serialize.is_valid():
            otp = serialize.validated_data.get("otp")
            saved_otp = request.session.get("otp")
            email = request.session.get("email")
            if otp == saved_otp:
                user = request.user
                user.email = email
                user.save()
                return Response("Email update successfully")
            else:
                return Response({"messege": "Invalid otp"})
        return Response(serialize.error_messages, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class VerifyMobileNumber(APIView):
    serializer_class = PhoneOtpSerializer

    @extend_schema(responses=PhoneOtpSerializer)
    def post(self, request):
        serializer = PhoneOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone_number")
            request.session["phone_number"] = phone
            print(phone)
            try:
                verification_sid = send_phone_sms(phone)
                print(verification_sid)
                request.session["verification_sid"] = verification_sid
                return Response(
                    {"sid": verification_sid}, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                print(e)
            return Response(
                {"msg": "somthing wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
class PhoneOtpVerificationView(APIView):
    serializer_class = OtpSerializer

    @extend_schema(responses=OtpSerializer)
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data.get("otp")
            verification_sid = request.session.get("verification_sid")
            try:
                verification_check = phone_otp_verify(verification_sid, otp)
                print(verification_check.status)
            except:
                return Response({"msg": "Something Went Wrong..."})
            if verification_check.status == "approved":
                entered_phone_number = request.session.get("phone_number")
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.phone = entered_phone_number
                user_profile.save()
                response_data = {
                    "msg": "your phone number is verifyed",
                }
                return Response(response_data)
            return Response(
                {"msg": "Something Went Wrong..."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseSearching(APIView):
    permission_classes = [AllowAny]

    serializer_class = CourseSearchSerializer
    @extend_schema(responses=CourseSearchSerializer)
    def get(self, reqeust):
        q = reqeust.GET.get("q")
        Q_base = Q()
        if q:
            Q_base = Q(heading__icontains=q) | Q(tutor__name__icontains=q)
        course = CourseDetailsModel.objects.filter(Q_base).select_related('tutor').prefetch_related("tutor__skills",'tutor__liveclassdetailsmodel_set')
        serializer = CourseSearchSerializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class TutorListing(APIView):
    permission_classes=[AllowAny]

    serializer_class = TutorListSerializer
    @extend_schema(responses=TutorListSerializer)
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
            serialzer = TutorListSerializer(tutors,many=True)
            return Response(serialzer.data)
        except Exception as e:
            return Response({"somthing wrong with your seralizer"})

        
class CourseListing(APIView):
    permission_classes = [AllowAny]

    sserializer_class = CourseListSerializer
    @extend_schema(responses=CourseListSerializer)
    def get(self, request):
        try:
            courses = CourseDetailsModel.objects.all()
        except CourseDetailsModel.DoesNotExist:
            raise Http404
            
        if courses:
            try:
                pagination = CustomUserListPagination()
                page_result = pagination.paginate_queryset(courses, request)
                serializer = CourseListSerializer(page_result, many=True)
                page_count = pagination.page.paginator.num_pages
                return Response({"data": serializer.data, "page_count": page_count})
            except Exception as e:
                print(e)
                return Response({"somting wrong with your serializer....."})
        return Response({"course not found"})
        

class LiveListing(APIView):
    permission_classes=[AllowAny]

    serializer_class = LiveListSerializer
    @extend_schema(responses=LiveListSerializer)
    def get(self,request):
        try:
            lives = LiveClassDetailsModel.objects.filter(
                session_status='Published'
            )

        except LiveClassDetailsModel.DoesNotExist:
            raise Http404("live not found")
        
        if lives:
            serializer = LiveListSerializer(lives,many=True)
            return Response(serializer.data)
        
        return Response({"somting wrong with your live serializer"})
    

# selecting one...............
class TutorSelect(APIView):
    permission_classes=[AllowAny]

    serializer_class = TutorSelectSerializer
    @extend_schema(responses=TutorSelectSerializer)
    def get(self, request,pk):
        try:
            tutor = TutorModel.objects.filter(id=pk).prefetch_related('coursedetailsmodel_set','liveclassdetailsmodel_set')
        except TutorModel.DoesNotExist:
            raise Http404('tutor not found')
        if tutor:
            serializer = TutorSelectSerializer(tutor,many=True)
            return Response(serializer.data)
        return Response('tutor not found')
    

class CourseSelect(APIView):
    permission_classes = [AllowAny]

    serializer_class = CourseSelectSerializer
    @extend_schema(responses=CourseSelectSerializer)
    def get(self, request, pk):
        try:
            course = CourseDetailsModel.objects.get(id=pk)
        except CourseDetailsModel.DoesNotExist:
            raise Http404("course not found")
        
        if course:
            serializer = CourseSelectSerializer(course)
            return Response(serializer.data)
        return Response("not fond")
    

class LiveSelect(APIView):
    permission_classes = [AllowAny]

    serializer_class = LiveSelectSerializer
    @extend_schema(responses=LiveSelectSerializer)
    def get(self, request, pk):
        try:
            live = LiveClassDetailsModel.objects.get(id=pk)
            print(live)
        except LiveClassDetailsModel.DoesNotExist:
            raise Http404('this live not fond')
        
        if live:
            serializer = LiveSelectSerializer(live)
            return Response(serializer.data)
        return Response("live not found")





class ShowCartView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CartItemSerializer
    @extend_schema(responses=CartItemSerializer)
    def get(self, request):
        try:
            items = CartItem.objects.filter(cart__user=request.user)
            if items:
                total_cost = 0
                for item in items:
                    cost = item.price
                    total_cost += cost
                serializer = CartItemSerializer(items,many=True)
                response = {
                    "data":serializer.data,
                    "total_cost":total_cost
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response("cart is empty")
        except CartItem.DoesNotExist:
            return Response("not found")
        


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CartItemSerializer
    @extend_schema(responses=CartItemSerializer)
    def post(self, request): 

        serializer = CartItemSerializer(data=request.data)
        
        if serializer.is_valid():
            new_course = serializer.validated_data.get('course')
            if CartItem.objects.filter(cart__user=request.user, course=new_course).exists():
                return Response("This item is already added to the cart", status=status.HTTP_400_BAD_REQUEST)
            
            items = CartItem.objects.create(
                cart = request.user.usercart,
                course = serializer.validated_data.get('course')
            )
            print(items.cart,items.course)
            return Response("item added")
        return Response(serializer.errors)
    


class Adtocart(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request, pk):    
        try:
            course = CourseDetailsModel.objects.get(id=pk)
        except CourseDetailsModel.DoesNotExist:
            raise Http404("this course not found")
        if CartItem.objects.filter(cart__user=request.user, course=course).exists():
            return Response("This item is already added to the cart", status=status.HTTP_400_BAD_REQUEST)
        if course:
            cart_item = CartItem(
                cart = request.user.usercart,
                course = course
            )
            cart_item.save()
            return Response("your item added")
        


class Checkout(APIView):
    def post(self, request):
        user = request.user 
        cartitems = CartItem.objects.all()
        if cartitems:
            total_cost = 0
            for item in cartitems:
                cost = item.price
                total_cost += cost
                

            return Response(total_cost)
        return Response("you should add a course to cart")