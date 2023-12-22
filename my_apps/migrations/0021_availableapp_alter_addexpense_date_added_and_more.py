# Generated by Django 4.2.1 on 2023-12-15 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0020_neweventmodel_event_date_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableApp',
            fields=[
                ('id_app', models.AutoField(primary_key=True, serialize=False)),
                ('app_name', models.TextField(default='')),
                ('app_describe', models.TextField(default='')),
                ('app_link', models.TextField(default='')),
                ('app_log_in', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 17, 46, 4, 636879)),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 17, 46, 4, 636879)),
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-15 17:46'),
        ),
    ]
