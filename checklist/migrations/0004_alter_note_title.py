# Generated by Django 4.1.7 on 2024-06-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0003_alter_note_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.TextField(),
        ),
    ]