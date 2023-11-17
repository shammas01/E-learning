from rest_framework import serializers
from . models import LiveClassDetailsModel,LiveClassContentsModel

class ListLiveSerializer(serializers.ModelSerializer):
    SESSION_TYPES = [
        ('One-to-Many', 'One-To-Many'),
        ('One-on-One', 'One-on-One'),
        ('Group', 'Group'),
    ]

    SESSION_STATUSES = [
        ('Planned', 'Planned'),
        ('Published', 'Published'),
    ]

    session_type = serializers.ChoiceField(choices=SESSION_TYPES,default='One-to-Many' )
    session_status= serializers.ChoiceField(choices=SESSION_STATUSES,default='Planned')
    class Meta:
        model = LiveClassDetailsModel
        fields = ('id',
                  'title',
                  'description',
                  'category',
                  'day_duration',
                  'session_type',
                  'class_start_datetime',
                  'class_duration',
                  'max_slots',
                  'available_slots',
                  'pricing',
                  'session_status')



class liveDetailUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = LiveClassDetailsModel
        exclude = ('id','teacher')
        