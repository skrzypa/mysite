# Generated by Django 4.2.1 on 2023-12-15 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0022_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 19, 52, 37, 440251)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 19, 52, 37, 440251)),
        ),
        migrations.AlterField(
            model_name='appphotos',
            name='photo',
            field=models.ImageField(upload_to='D:\\Rozne\\Kody\\6. Projekty WWW\\data\\homepage'),
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-15 19:52'),
        ),
    ]
