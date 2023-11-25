from django.http import Http404
from rest_framework.views import APIView
from . serializers import ListLiveSerializer,liveDetailUpdateSerializer
from tutor.permissions import IsTutorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from . models import LiveClassDetailsModel
from tutor.models import TutorModel
from rest_framework.response import Response
from rest_framework import status
from live.module.smtp import send_email_live_confierm
from drf_spectacular.utils import extend_schema
# Create your views here.


class LiveDetailListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTutorOrReadOnly]

    serializer_class = ListLiveSerializer
    @extend_schema(responses=ListLiveSerializer)
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
                    session_type = serializer.validated_data.get('session_type'),
                    class_start_datetime = serializer.validated_data.get('class_start_datetime'),
                    class_duration = serializer.validated_data.get('class_duration'),
                    max_slots = serializer.validated_data.get('max_slots'),
                    available_slots = serializer.validated_data.get('max_slots'),
                    pricing = serializer.validated_data.get('pricing'),
                    created_datetime = serializer.validated_data.get('created_datetime'),
                    last_updated_datetime = serializer.validated_data.get('last_updated_datetime')
                )
                response = {"message":"Live details successfull crated","data":serializer.data}
                return Response(response,status=status.HTTP_201_CREATED)
            return Response("somthing wrong with your account. contact admin")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    serializer_class = ListLiveSerializer
    @extend_schema(responses=ListLiveSerializer)
    def get(self, request):
        data = LiveClassDetailsModel.objects.filter(teacher=request.user.tutormodel)
        serializer = ListLiveSerializer(data,many=True)
        return Response(serializer.data)
        
    
class LiveDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsTutorOrReadOnly]
    def get_object(self,pk):
        try:
            return LiveClassDetailsModel.objects.get(id=pk, teacher=self.request.user.tutormodel)
        except LiveClassDetailsModel.DoesNotExist:
            raise Http404("not found")
    

    serializer_class = liveDetailUpdateSerializer
    @extend_schema(responses=liveDetailUpdateSerializer)
    def get(self, request, pk):
        data = self.get_object(pk)
        st=data.session_status
        print("#############",st)
        serializer = liveDetailUpdateSerializer(data)
        return Response(serializer.data)
    

    serializer_class = liveDetailUpdateSerializer
    @extend_schema(responses=liveDetailUpdateSerializer)
    def put(self, request, pk):
        live_details = self.get_object(pk)
        statuss =live_details.session_status
        print(">>>>>>>>>>>>>>>>",statuss)
        serializer = liveDetailUpdateSerializer(live_details,data=request.data,partial=True)
        session = LiveClassDetailsModel.objects.get(teacher=request.user.tutormodel)
        if serializer.is_valid():

            if session.session_status and session.session_status != 'Planned':
                return Response("Cannot update once session status is Published", status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            response = {"message":"successfully updated","data":serializer.data}
            return Response(response,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, requset, pk):
        live_details = self.get_object(pk)
        live_details.delete()
        return Response("Deleted your live session",status=status.HTTP_404_NOT_FOUND)
    

