# Generated by Django 4.1.7 on 2023-09-03 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0017_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_open', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 3, 9, 7, 46, 148455)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 3, 9, 7, 46, 147455)),
        ),
    ]
