# Generated by Django 4.2.6 on 2023-11-09 07:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0003_alter_coursecontentmodel_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursedetailsmodel",
            name="heading",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
