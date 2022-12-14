# Generated by Django 3.2.15 on 2022-09-11 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nbp", "0002_alter_exchangeratepln_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangeratepln",
            name="currency",
            field=models.CharField(
                choices=[
                    ("USD", "US Dollar"),
                    ("EUR", "Euro"),
                    ("CHF", "Swiss Franc"),
                    ("JPY", "Japanese Yen"),
                ],
                max_length=3,
                verbose_name="currency",
            ),
        ),
    ]
