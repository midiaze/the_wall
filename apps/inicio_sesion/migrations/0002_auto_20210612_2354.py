# Generated by Django 2.2.4 on 2021-06-13 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio_sesion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]