# Generated by Django 4.1.7 on 2024-12-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('split_the_bills', '0004_addtogroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splitthebills',
            name='bills',
            field=models.JSONField(default=list),
        ),
    ]
