# Generated by Django 4.2.6 on 2023-11-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutormodel',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, related_name='tutors', to='tutor.skillmodel'),
        ),
    ]