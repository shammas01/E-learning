# Generated by Django 4.2.6 on 2023-11-03 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_alter_tutormodel_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutormodel',
            name='phone',
            field=models.CharField(max_length=13, null=True, unique=True),
        ),
    ]
