# Generated by Django 4.1.7 on 2023-05-26 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_apps', '0003_addexpense_addexpensegroup_addfriendtoexpensegroup_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addexpense',
            old_name='expense',
            new_name='expense_group_id',
        ),
        migrations.RenameField(
            model_name='addfriendtoexpense',
            old_name='expense',
            new_name='expense_id',
        ),
    ]
