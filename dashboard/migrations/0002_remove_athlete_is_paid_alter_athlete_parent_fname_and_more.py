# Generated by Django 4.2 on 2024-03-11 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='is_paid',
        ),
        migrations.AlterField(
            model_name='athlete',
            name='Parent_fname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='Parent_lname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='address',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='age',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='age', to='dashboard.age'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='designation',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='parent_nin',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='parent_phone_number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='athlete',
            name='photo',
            field=models.ImageField(default=1, upload_to='athlete_photos/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='fname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='lname',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='nin',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='school',
            name='phone_number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]