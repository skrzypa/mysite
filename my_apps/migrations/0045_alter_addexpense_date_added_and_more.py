# Generated by Django 4.1.7 on 2023-12-21 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0044_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpense',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='addexpensegroup',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-21 18:51'),
        ),
    ]
