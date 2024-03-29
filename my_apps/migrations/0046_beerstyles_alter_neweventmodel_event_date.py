# Generated by Django 4.1.7 on 2023-12-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0045_alter_addexpense_date_added_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerStyles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('style_name', models.TextField(default='')),
                ('max_carbonation', models.FloatField(default=0)),
                ('min_carbonation', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Beer style',
                'verbose_name_plural': 'Beer styles',
            },
        ),
        migrations.AlterField(
            model_name='neweventmodel',
            name='event_date',
            field=models.DateTimeField(default='2023-12-22 19:30'),
        ),
    ]
