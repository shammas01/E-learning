from rest_framework import serializers
from . models import (CourseDetailsModel,CourseContentModel)


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContentModel
        fields = ['id','course_id','title','description','document','video','order']


class CourseDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseDetailsModel
        fields = ['heading','contents','description','duration','language','catogory']
        

    def update(self, instance, validated_data):
    
        instance.heading = validated_data.get('heading',instance.heading)
        instance.contents = validated_data.get('contents',instance.contents)
        instance.description = validated_data.get('description',instance.description)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.language = validated_data.get('language',instance.language)

        # print(validated_data)
        # content = instance.course_content.all()
        # if content:
        #     for c in content:
        #         validated_cource_content_data = validated_data.get('course_content',{})
        #         print(validated_cource_content_data)
        #         c.title = validated_cource_content_data.get('title',c.title)
        #         c.description = validated_cource_content_data.get('description',c.description)
        #         c.document = validated_cource_content_data.get('document',c.document)
        #         c.video = validated_cource_content_data.get('video',c.video)
        #         c.order = validated_cource_content_data.get('order',c.order)
        #         c.save()
        instance.save()
        return instance