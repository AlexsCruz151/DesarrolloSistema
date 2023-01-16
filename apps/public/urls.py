from django.urls import path
from .views import CategoriaView, UpdateCategoria

app_name = 'public'
urlpatterns = [
    path('categoria/', CategoriaView.as_view(), name='categoria'),
    path('updatecategoria/', UpdateCategoria, name='updateCategoria'),
]
