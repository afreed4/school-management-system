# Generated by Django 5.1.4 on 2024-12-13 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_rename_certifiation_librarian_certification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachers',
            old_name='tecahing_position',
            new_name='teaching_position',
        ),
    ]
