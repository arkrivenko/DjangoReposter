# Generated by Django 4.2.3 on 2023-07-15 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgapp', '0006_mediafile_created_at_mediafile_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeldata',
            name='description',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 10, 23, 17, 134370)),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='task_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 10, 23, 17, 134370)),
        ),
    ]
