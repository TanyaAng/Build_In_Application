# Generated by Django 4.1.1 on 2022-11-13 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_logactivity_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logactivity',
            name='action',
            field=models.CharField(max_length=21),
        ),
    ]