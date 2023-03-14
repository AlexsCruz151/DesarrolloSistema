from django.urls import path
from .views import *

app_name = 'public'
urlpatterns = [
    path('categoria/', CategoriaView.as_view(), name='categoria'),
    path('updatecategoria/', UpdateCategoria, name='updateCategoria'),
    path('piezas/', PiezasView.as_view(), name='piezas'),
    path('updatepiezas/', UpdatePieza, name='updatePieza'),
    path('getpieza/', GetPieza, name='getPieza'),
    path('productopiezas/', ProductoPiezasView.as_view(), name='productopiezas'),
    path('empresa/', EmpresasView.as_view(), name='empresa'),
    path('actualizarempresa/', UpdateEmpresa, name='updateEmpresa'),
    path('bodega/', BodegasView.as_view(), name='bodega'),
    path('updatebodega/', UpdateBodega, name='updateBodega'),
    path('entradapiezas/', EntradaPiezasView.as_view(), name='entradaPiezas'),
    path('getdetalleentrada/', GetDetalleEntrada, name='detalleEntrada'),
    path('productos/', ProductosView.as_view(), name='productos'),
    path('manofacturaproductos/', ManofacturaProductosView.as_view(), name='manofacturaProductos'),
    path('getmanofacturaproductos/', GetManofacturaProductos, name='getmanofacturaproductos'),
    path('updatemanofacturaproductos/', UpdateManofacturaProductos, name='updatemanofacturaproductos'),
]
