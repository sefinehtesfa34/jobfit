# Generated by Django 4.1.7 on 2023-04-16 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_alter_customeuser_timestamp_alter_job_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='link',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='customeuser',
            name='timestamp',
            field=models.DateField(default=datetime.date(2023, 4, 16)),
        ),
        migrations.AlterField(
            model_name='job',
            name='timestamp',
            field=models.DateField(default=datetime.date(2023, 4, 16)),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='timestamp',
            field=models.DateField(default=datetime.date(2023, 4, 16)),
        ),
    ]
