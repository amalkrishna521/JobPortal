# Generated by Django 5.0.2 on 2024-06-08 02:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_recruiter'),
    ]

    operations = [
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('salary', models.FloatField(max_length=100)),
                ('image', models.FileField(upload_to='')),
                ('description', models.CharField(max_length=300)),
                ('experiance', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=400)),
                ('skills', models.CharField(max_length=100)),
                ('creationdate', models.DateField(max_length=40, null=True)),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.recruiter')),
            ],
        ),
    ]
