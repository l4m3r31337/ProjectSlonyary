# Generated by Django 5.1.3 on 2024-12-01 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_users_internship_alter_internship_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Internship',
            new_name='InternshipModel',
        ),
    ]
