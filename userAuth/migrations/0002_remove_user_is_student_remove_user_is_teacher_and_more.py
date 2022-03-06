# Generated by Django 4.0.3 on 2022-03-04 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mailing_address',
        ),
        migrations.AddField(
            model_name='user',
            name='contact_info',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='user_ip',
            field=models.BooleanField(default=False),
        ),
    ]