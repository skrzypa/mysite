# Generated by Django 4.1.7 on 2024-05-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NBP_API',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_addded', models.DateTimeField(auto_now=True)),
                ('currencies', models.JSONField()),
            ],
        ),
    ]