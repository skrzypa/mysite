# Generated by Django 4.1.7 on 2023-12-23 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DescribeApp',
            fields=[
                ('id_app', models.AutoField(primary_key=True, serialize=False)),
                ('app_name', models.TextField(default='')),
                ('app_describe', models.TextField(default='')),
                ('app_photo', models.ImageField(upload_to='homepage/')),
                ('app_link', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Describe App',
                'verbose_name_plural': 'Describe App',
            },
        ),
    ]
