# Generated by Django 4.0.3 on 2022-04-30 14:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_client_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_end',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_start',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
