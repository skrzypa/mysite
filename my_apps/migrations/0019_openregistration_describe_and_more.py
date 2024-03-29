# Generated by Django 4.1.7 on 2023-09-03 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0018_openregistration_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='openregistration',
            name='describe',
            field=models.TextField(default="The registration is open? (Don't create new entry, edit this one)"),
        ),
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 3, 9, 12, 18, 828117)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 3, 9, 12, 18, 827119)),
        ),
    ]
