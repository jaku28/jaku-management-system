# Generated by Django 2.0.2 on 2021-07-24 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0044_workshop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='call',
            name='workshops',
        ),
    ]
