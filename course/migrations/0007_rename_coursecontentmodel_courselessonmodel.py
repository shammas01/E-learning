# Generated by Django 4.2.6 on 2023-11-14 09:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0006_alter_coursecontentmodel_title"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CourseContentModel",
            new_name="CourseLessonModel",
        ),
    ]
