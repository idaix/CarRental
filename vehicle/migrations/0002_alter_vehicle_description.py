# Generated by Django 4.0.3 on 2022-04-15 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='description',
            field=models.TextField(blank=True, help_text='Small description (1000)', max_length=1000, null=True),
        ),
    ]