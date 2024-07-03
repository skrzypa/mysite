# Generated by Django 4.1.7 on 2024-06-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0007_note_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='invited_friends',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]