# Generated by Django 4.2 on 2024-05-09 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_team_team_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='team_age',
        ),
    ]
