# Generated by Django 4.1.1 on 2022-11-13 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildinproject',
            name='project_phase',
            field=models.CharField(blank=True, choices=[('RandD', 'Research and Development'), ('PD', 'Preliminary Design'), ('SD', 'Schematic Design'), ('DD', 'Design Development'), ('CD', 'Construction Document'), ('OTHER', 'Other')], max_length=5, null=True),
        ),
    ]
