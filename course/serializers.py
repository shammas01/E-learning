from rest_framework import serializers
from . models import (CourseDetailsModel,CourseLessonModel)

class CourseDetailsListCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseDetailsModel
        fields = ['id','heading','contents','description','duration','language','price']
        

    


class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetailsModel
        exclude = ('tutor',)
    

    def update(self, instance, validated_data):
        instance.heading = validated_data.get('heading',instance.heading)
        instance.contents = validated_data.get('contents',instance.contents)
        instance.description = validated_data.get('description',instance.description)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.language = validated_data.get('language',instance.language)
        instance.catogory = validated_data.get('catogory',instance.catogory)
        instance.price = validated_data.get('price',instance.price)

        instance.save()
        return instance





class ContentListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonModel
        exclude = ('course_id',)



class LessonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonModel
        exclude = ('course_id',)


