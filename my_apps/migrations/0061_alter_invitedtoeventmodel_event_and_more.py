# Generated by Django 4.1.7 on 2024-04-28 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_apps', '0060_alter_invitedtoeventmodel_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitedtoeventmodel',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_apps.neweventmodel'),
        ),
        migrations.CreateModel(
            name='InvitedToEventModelNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_invitation', models.BooleanField(default=False)),
                ('decline_invitation', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_apps.neweventmodelnew')),
                ('invited_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
