# Generated by Django 4.0.3 on 2022-03-04 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0002_remove_user_is_student_remove_user_is_teacher_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='contact_info',
            new_name='holidays',
        ),
    ]
