# Generated by Django 3.2.9 on 2022-03-05 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPosts', '0002_post_created_at_post_is_active_post_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='postlikes',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
