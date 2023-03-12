# Generated by Django 3.2.5 on 2023-02-19 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0005_auto_20230212_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodega',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_bodega', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoria',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_categoria', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='empresa',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_empresa', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='piezas',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_piezas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='piezasprecio',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_piezasprecio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productos',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_productos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productospiezas',
            name='usuario_sesion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuario_sesion_productospiezas', to=settings.AUTH_USER_MODEL),
        ),
    ]