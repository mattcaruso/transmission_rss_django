# Generated by Django 4.0.2 on 2022-02-13 20:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0002_alter_feed_created_alter_feed_last_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 13, 20, 29, 57, 133382, tzinfo=utc)),
        ),
    ]