# Generated by Django 4.0.3 on 2022-04-16 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0002_alter_agency_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='lon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='agency.agency'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]