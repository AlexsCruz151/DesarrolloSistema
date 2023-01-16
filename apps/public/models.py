from django.db import models
from ..core.models import Base

class Categoria(Base):
    descripcion = models.CharField(verbose_name='Descripción', max_length=50, blank=False, null=False)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'WebSite'

    def __str__(self):
        return 'WebSite'