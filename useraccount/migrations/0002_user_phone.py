# Generated by Django 4.2.6 on 2023-10-31 04:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("useraccount", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
