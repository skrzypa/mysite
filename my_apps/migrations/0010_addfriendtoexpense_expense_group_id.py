# Generated by Django 4.1.7 on 2023-05-27 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0009_addexpense_repaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='addfriendtoexpense',
            name='expense_group_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='my_apps.addexpensegroup'),
            preserve_default=False,
        ),
    ]
