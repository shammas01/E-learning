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

        instance.max_slots = validated_data.get("max_slots", instance.max_slots)
        instance.available_slots = validated_data.get("max_slots", instance.max_slots)
            
        if 'session_status' in validated_data and validated_data['session_status'] == 'Published':
            print("oklasjdfljasdlfkjals;dkfjalskdflaskdfj")
            subject = f"Confirmation message for {instance.title} live session"
            message = f"Congratulations! Your live session {instance.title} has been activated.\n\n"
            message += f"If you wish to update your live session before publishing, you can do so.\n\n"
            message += f"Your published date is: {instance.last_updated_datetime}"

            teacher = instance.teacher
            print(teacher)
            send_email_live_confierm(subject=subject,message=message,email=teacher)
        return super().update(instance, validated_data)