# Generated by Django 4.2.6 on 2023-11-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0003_tutormodel_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutormodel',
            name='is_block',
            field=models.BooleanField(default=False),
        ),
    ]