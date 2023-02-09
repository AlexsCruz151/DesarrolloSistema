import uuid
from django.db import models
from ..core.models import Base

class Empresa(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    logo = models.ImageField(upload_to='empresa')
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Empresa'

    def __str__(self):
        return 'Empresa'

class Categoria(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    empresa = models.ForeignKey(Empresa,on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categorias'

    def __str__(self):
        return 'Categorias'


class Piezas(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    codigo = models.CharField(verbose_name='codigo', max_length=20,null=False,blank=False)
    imagen = models.ImageField(upload_to='piezas')
    cantidad = models.IntegerField(null=False, default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Piezas'

    def __str__(self):
        return 'Piezas'


class Productos(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    imagen = models.ImageField(upload_to='productos')
    cantidad = models.IntegerField(null=False, default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Productos'

    def __str__(self):
        return 'Productos'

class Productospiezas(Base):
    producto = models.ForeignKey(Productos,on_delete=models.PROTECT)
    pieza = models.ForeignKey(Piezas,on_delete=models.PROTECT)
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Productospiezas'

    def __str__(self):
        return 'Productos Piezas'
