# Generated by Django 3.2.5 on 2023-02-12 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0003_piezasprecio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_grabacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('descripcion', models.CharField(max_length=50, verbose_name='Descripción')),
                ('codigo', models.CharField(max_length=20, verbose_name='codigo')),
                ('estado', models.IntegerField(default=1)),
                ('usuario_grabacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_grabacion_bodega', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_modificacion_bodega', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bodega',
            },
        ),
    ]
