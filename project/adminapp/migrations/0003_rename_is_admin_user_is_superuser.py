# Generated by Django 5.1.4 on 2024-12-12 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_rename_is_non_teaching_staff_user_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='is_superuser',
        ),
    ]
