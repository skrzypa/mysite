# Generated by Django 4.1.7 on 2023-12-19 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0033_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 13, 9, 48, 706460)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 13, 9, 48, 705460)),
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-19 13:09'),
        ),
    ]
