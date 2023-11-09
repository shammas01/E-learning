from . models import (
            CategoryModel,
            CourseContentModel,
            CourseDetailsModel,
            CourseRatingModel,
            LiveClassContentsModel,
            LiveClassDetailsModel)
from . serializers import CourseContentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CourseContentSerializer(data=request.data)
        tutor = serializer.data.get('tutor')
        if tutor.approve is True:
            if serializer.is_valid():
                course = CourseContentModel.objects.create(
                    tutor = request.user,
                    heading = serializer.validated_data.get('heading'),
                )
       
    