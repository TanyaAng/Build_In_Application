# Generated by Django 4.1.1 on 2022-10-09 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=30)),
                ('task_name', models.CharField(max_length=60)),
                ('time_estimation', models.PositiveIntegerField(blank=True, null=True)),
                ('is_ready_for_markups', models.BooleanField()),
                ('is_approved', models.BooleanField()),
                ('is_issued', models.BooleanField()),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.buildinproject')),
            ],
        ),
    ]
