# Generated by Django 5.1.4 on 2024-12-13 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_rename_certifiation_staff_certification_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librarian',
            old_name='certifiation',
            new_name='certification',
        ),
    ]
