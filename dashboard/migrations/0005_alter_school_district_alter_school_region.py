# Generated by Django 4.2 on 2024-03-19 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('dashboard', '0004_alter_athlete_mname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='district',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='district', to='accounts.district'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='region', to='accounts.region'),
            preserve_default=False,
        ),
    ]
