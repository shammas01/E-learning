from rest_framework import serializers
from . models import LiveClassDetailsModel,LiveClassContentsModel

class ListLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClassDetailsModel
        fields = ('title',
                  'description',
                  'category',
                  'day_duration',
                  'session_type',
                  'class_start_datetime',
                  'class_duration',
                  'max_slots',
                  'pricing',
                  'session_status')
        