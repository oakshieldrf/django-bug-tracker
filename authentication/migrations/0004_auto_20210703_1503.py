# Generated by Django 2.2.10 on 2021-07-03 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210622_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='horasTrabajo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]