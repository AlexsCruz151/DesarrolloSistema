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

class Bodega(Base):
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=True, null=True)
    codigo = models.CharField(verbose_name='codigo', max_length=20,null=False,blank=False)
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Bodega'

    def __str__(self):
        return 'Bodega'

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
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Piezas'

    def __str__(self):
        return 'Piezas'

class PiezasPrecio(Base):
    pieza = models.ForeignKey(Piezas, on_delete=models.PROTECT)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    cantidad = models.IntegerField(null=False, default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Piezas Precios'

    def __str__(self):
        return 'Piezas Precio'


class EntradaPiezas(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Entrada Piezas'

    def __str__(self):
        return 'Entradas Piezas'

class DetalleEntradaPiezas(Base):
    pieza_precio = models.ForeignKey(PiezasPrecio,on_delete=models.PROTECT)
    entrada_pieza = models.ForeignKey(EntradaPiezas,on_delete=models.PROTECT)
    cantidad = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = 'Detalle Entradas Piezas'

    def __str__(self):
        return 'Detalle Entradas Piezas'


class Productos(Base):
    codigo = models.CharField(verbose_name='codigo', max_length=20, null=False, blank=False)
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    imagen = models.ImageField(upload_to='productos')
    cantidad = models.IntegerField(null=False, default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    tipo = models.IntegerField(null=False,default=1) # 1: Productos con piezas.  2: Productos normales
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Productos'

    def __str__(self):
        return 'Productos'

class Productospiezas(Base):
    producto = models.ForeignKey(Productos,on_delete=models.PROTECT)
    pieza = models.ForeignKey(Piezas,on_delete=models.PROTECT)
    cantidad = models.IntegerField(null=False,default=1)
    estado = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Productospiezas'

    def __str__(self):
        return 'Productos Piezas'
