# Generated by Django 4.2 on 2024-02-27 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('min_age', models.IntegerField(blank=True, null=True)),
                ('max_age', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('mname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('lin', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'male'), ('Female', 'female')], max_length=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='athlete_photos/')),
                ('Parent_fname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Parent_lname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('parent_phone_number', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('parent_nin', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('designation', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('relationship', models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Other', 'Other')], max_length=15, null=True)),
                ('is_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10, null=True)),
                ('age', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='age', to='dashboard.age')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=19)),
                ('badge', models.ImageField(blank=True, null=True, upload_to='badge/')),
                ('EMIS', models.CharField(max_length=100, unique=True)),
                ('center_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('lname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('fname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('nin', models.CharField(default='', max_length=20)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='badge/')),
                ('gfname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('glname', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('gemail', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('gphone', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('gnin', models.CharField(default='', max_length=20)),
                ('gdate_of_birth', models.DateField()),
                ('ggender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('gphoto', models.ImageField(blank=True, null=True, upload_to='badge/')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcounty', to='accounts.city')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district', to='accounts.district')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='county', to='accounts.municipality')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region', to='accounts.region')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='school_official',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('nin', models.CharField(default='', max_length=20)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('role', models.CharField(blank=True, choices=[('Coach', 'Coach'), ('Teacher', 'Teacher'), ('Assistant Games Teacher', 'Assistant Games Teacher'), ('Assistant Head Teacher', 'Assistant Head Teacher'), ('Nurse', 'Nurse'), ('Doctor', 'Doctor'), ('District Education Officer', 'District Education Officer'), ('District Sports Officer', 'District Sports Officer')], max_length=40, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='badge/')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school', to='dashboard.school')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('athletes', models.ManyToManyField(to='dashboard.athlete')),
            ],
        ),
        migrations.AddField(
            model_name='athlete',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom', to='dashboard.classroom'),
        ),
        migrations.AddField(
            model_name='athlete',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schooler', to='dashboard.school'),
        ),
        migrations.AddField(
            model_name='athlete',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sport', to='accounts.sport'),
        ),
    ]
