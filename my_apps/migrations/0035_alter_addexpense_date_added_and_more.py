# Generated by Django 4.1.7 on 2023-12-19 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0034_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 15, 34, 5, 718264)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 15, 34, 5, 718264)),
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-19 15:34'),
        ),
    ]
