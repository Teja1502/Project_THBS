# Generated by Django 4.2.7 on 2024-01-05 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registerApp", "0006_remove_userprofile_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="location",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
