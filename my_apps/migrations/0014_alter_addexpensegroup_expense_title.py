# Generated by Django 4.1.7 on 2023-05-27 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0013_addexpense_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpensegroup',
            name='expense_title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
