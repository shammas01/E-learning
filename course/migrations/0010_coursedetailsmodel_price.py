# Generated by Django 4.2.6 on 2023-11-25 06:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0009_remove_liveclassdetailsmodel_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursedetailsmodel",
            name="price",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
