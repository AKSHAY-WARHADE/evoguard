# Generated by Django 4.1.5 on 2024-03-29 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0003_complaint_latitude_complaint_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='longitude',
        ),
    ]
