# Generated by Django 4.0.3 on 2022-05-13 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0011_agency_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='image',
        ),
    ]