from django.urls import path
from .views import CategoriaView

app_name = 'public'
urlpatterns = [
    path('', CategoriaView.as_view(), name='categoria'),
]
