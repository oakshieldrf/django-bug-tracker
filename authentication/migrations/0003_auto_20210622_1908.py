# Generated by Django 2.2.10 on 2021-06-23 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210622_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='horasTrabajo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userextend',
            name='ultimoUpdate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]