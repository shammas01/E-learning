# Generated by Django 4.2.6 on 2023-12-01 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("course", "0010_coursedetailsmodel_price"),
        (
            "userdashboad",
            "0002_cartitem_usercart_delete_usercartmodel_cartitem_cart_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderPlaced",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordered_date", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="course.coursedetailsmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]