# Generated by Django 2.0.2 on 2020-06-06 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='call',
            options={'verbose_name': 'convocatoria'},
        ),
        migrations.AlterModelOptions(
            name='entity',
            options={'verbose_name': 'entidad', 'verbose_name_plural': 'entidades'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'proyecto'},
        ),
        migrations.AlterField(
            model_name='call',
            name='rules',
            field=models.FileField(upload_to='', verbose_name='bases'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nombre'),
        ),
    ]
