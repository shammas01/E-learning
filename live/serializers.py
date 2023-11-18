from rest_framework import serializers
from . models import LiveClassDetailsModel,LiveClassContentsModel
from live.module.smtp import send_email_live_confierm
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
    SESSION_STATUSES = [
        ('Planned', 'Planned'),
        ('Published', 'Published'),
    ]
    session_status= serializers.ChoiceField(choices=SESSION_STATUSES,default='Planned')
    class Meta:
        model = LiveClassDetailsModel
        exclude = ('id','teacher')
        
    def update(self, instance, validated_data):
        print(validated_data)
             
        if 'session_status' in validated_data and validated_data['session_status'] == 'Published':

            print("oklasjdfljasdlfkjals;dkfjalskdflaskdfj")
            subject = "confirm message for this live session"
            message = """congragulation your live session has been activated

                # if you want to update your live session befor publishing.

                """
            teacher = instance.teacher
            print(teacher)
            send_email_live_confierm(subject=subject,message=message,email=teacher)
            print(send_email_live_confierm)
            return super().update(instance, validated_data)