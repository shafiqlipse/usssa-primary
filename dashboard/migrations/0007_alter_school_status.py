# Generated by Django 4.2 on 2024-03-21 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_school_district_alter_school_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=19),
        ),
    ]