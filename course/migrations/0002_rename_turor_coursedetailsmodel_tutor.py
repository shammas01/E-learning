# Generated by Django 4.2.6 on 2023-11-09 06:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coursedetailsmodel",
            old_name="turor",
            new_name="tutor",
        ),
    ]
