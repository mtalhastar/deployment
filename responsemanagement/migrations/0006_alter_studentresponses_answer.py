# Generated by Django 4.2.6 on 2023-12-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsemanagement', '0005_modelresponse_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresponses',
            name='answer',
            field=models.TextField(),
        ),
    ]