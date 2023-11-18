from django.test import TestCase

# Create your tests here.

def update(self, instance, validated_data):
            instance.title = validated_data.get("title", instance.title)
            instance.description = validated_data.get("description", instance.description)
            instance.day_duration = validated_data.get("day_duration", instance.day_duration)
            instance.session_type = validated_data.get("session_type", instance.session_type)
            instance.class_start_datetime = validated_data.get("class_start_datetime", instance.class_start_datetime)
            instance.class_duration = validated_data.get("class_duration", instance.class_duration)
            instance.max_slots = validated_data.get("max_slots", instance.max_slots)
            instance.available_slots = validated_data.get("max_slots", instance.max_slots)
            instance.pricing = validated_data.get("pricing", instance.pricing)
            instance.session_status = validated_data.get("session_status", instance.session_status)
            
            validated_category_data = validated_data.pop("category", None)
            category = instance.category
            if validated_category_data:
                instance.liveclassdetailsmodel.category = validated_category_data.get(
                    "category", instance.liveclassdetailsmodel.category
                )
                category.save()
            instance.save()
            return instance