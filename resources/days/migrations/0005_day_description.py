# Generated by Django 3.2.8 on 2021-11-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("days", "0004_day_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="day",
            name="description",
            field=models.TextField(default="Please Add Description..."),
        ),
    ]