# Generated by Django 2.2.10 on 2021-06-08 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField(max_length=200)),
                ('horasTrabajo', models.TimeField()),
                ('miembros', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_miembros', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoSolicitud', models.CharField(choices=[('incidencia', 'Incidencia'), ('mejora', 'Mejora')], default='incidencia', max_length=20)),
                ('descripcion', models.TextField(max_length=1000)),
                ('tituloIncidente', models.CharField(max_length=200)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('abierto', 'Abierto'), ('resuelto', 'Resuelto'), ('cerrado', 'Cerrado'), ('eliminado', 'Eliminado')], default='abierto', max_length=20)),
                ('severidad', models.CharField(choices=[('P1', 'Crítico'), ('P2', 'Alto'), ('P3', 'Moderado'), ('P4', 'Bajo'), ('P5', 'Informativo')], default='P5', max_length=20)),
                ('horasEstimadas', models.TimeField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sistema_incidencia', to=settings.AUTH_USER_MODEL)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_incidencias', to='app.Equipo')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidencia_responsables', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
