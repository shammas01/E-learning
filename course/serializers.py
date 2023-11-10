from rest_framework import serializers
from . models import (CourseDetailsModel,CourseContentModel)

class CourseDetailsListCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseDetailsModel
        fields = ['id','heading','contents','description','duration','language','catogory']
        

    def update(self, instance, validated_data):
        instance.heading = validated_data.get('heading',instance.heading)
        instance.contents = validated_data.get('contents',instance.contents)
        instance.description = validated_data.get('description',instance.description)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.language = validated_data.get('language',instance.language)
        instance.save()
        return instance



class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContentModel
        fields = '__all__'



class CourseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDetailsModel
        exclude = ('tutor',)



