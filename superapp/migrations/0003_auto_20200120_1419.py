# Generated by Django 2.2 on 2020-01-20 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('MENTOR', 'MENTOR/INVESTOR'), ('STUDENT', 'STUDENT'), ('EXPLORER', 'EXPLORER')], default='EXPLORER', max_length=200),
        ),
    ]
