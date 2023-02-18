import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from ..public.models import Categoria, Piezas, Empresa, Bodega, PiezasPrecio
from django.db import transaction, connection
from django.http import HttpResponseNotFound, JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
import json
import decimal
#g


class CategoriaView(LoginRequiredMixin, TemplateView):
    template_name = 'public/categoriaView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        opcionError = 0  # 1: Existe usuario

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))

                try:
                    Categoria.objects.get(descripcion=descripcion)
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la categoría: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = bool(request.POST.get('estadoActivo'))
                    categoria = Categoria(descripcion=descripcion, estado=estadoActivo)
                    categoria.save()
                    mensaje = 'Categoría guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})


def UpdateCategoria(request, *args, **kwargs):
    error = False
    mensaje = ''

    id = str(request.POST.get('id'))
    categoria = Categoria.objects.get(id=id)

    try:
        with transaction.atomic():
            categoria.descripcion = str(request.POST.get("descripcion"))
            categoria.estado = bool(request.POST.get("estadoActivo"))
            categoria.save()

            mensaje = 'Categoria Actualizada'

    except Exception as e:
        error = True
        mensaje = str(e)

    return JsonResponse({'error': error, 'mensaje': mensaje})

#*** PIEZAS ***#

class PiezasView(LoginRequiredMixin, TemplateView):
    template_name = 'public/piezasView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['piezas'] = Piezas.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        opcionError = 0  # 1: Existe usuario

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))
                codigoReferencia = str(request.POST.get('codigoReferencia'))


                try:
                    Piezas.objects.get(Q(descripcion=descripcion) | Q(codigo=codigoReferencia),estado__in=[0,1])
                    opcionError = 1
                    error = True
                    mensaje = 'Ya existe la pieza: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = int(request.POST.get('estadoActivo'))
                    piezas = Piezas(codigo=codigoReferencia, descripcion=descripcion, estado=estadoActivo)
                    imagen = request.FILES['file']
                    piezas.imagen = imagen
                    piezas.save()
                    mensaje = 'Pieza guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': opcionError})

def UpdatePieza(request, *args, **kwargs):
    error = False
    mensaje = ''

    id = str(request.POST.get('id'))
    piezas = Piezas.objects.get(id=id)

    try:
        with transaction.atomic():
            piezas.descripcion = str(request.POST.get("descripcion"))
            piezas.estado = bool(request.POST.get("estadoActivo"))
            piezas.save()
            mensaje = 'Pieza Actualizada'

    except Exception as e:
        error = True
        mensaje = str(e)

    return JsonResponse({'error': error, 'mensaje': mensaje})

def GetPieza(request, *args, **kwargs):

    get = int(request.POST.get('get'))

    if get == 1: # Extraer detalle de precios
        detalle_precios = PiezasPrecio.objects.filter(pieza__id=1)
        return JsonResponse(list(detalle_precios),safe=False)

class ProductoPiezasView(LoginRequiredMixin, TemplateView):
    template_name = 'public/productoPiezasView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['piezas'] = Piezas.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        opcionError = 0  # 1: Existe usuario

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))

                try:
                    Piezas.objects.get(descripcion=descripcion)
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la pieza: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = bool(request.POST.get('estadoActivo'))
                    piezas = Piezas(descripcion=descripcion, estado=estadoActivo)
                    piezas.save()
                    mensaje = 'Pieza guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})

def UpdateProductoPiezas(request, *args, **kwargs):
    error = False
    mensaje = ''

    id = str(request.POST.get('id'))
    piezas = Piezas.objects.get(id=id)

    try:
        with transaction.atomic():
            piezas.descripcion = str(request.POST.get("descripcion"))
            piezas.estado = bool(request.POST.get("estadoActivo"))
            piezas.save()

            mensaje = 'Pieza Actualizada'

    except Exception as e:
        error = True
        mensaje = str(e)

    return JsonResponse({'error': error, 'mensaje': mensaje})


#*** EMPRESAS ***#

class EmpresasView(LoginRequiredMixin, TemplateView):
    template_name = 'public/empresasView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresas'] = Empresa.objects.filter(Q(estado=1) | Q(estado=0))
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        optionError = 0  # 1: Existe empresa

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion')).upper()

                try:
                    Empresa.objects.get(descripcion=descripcion,estado__in=[0,1])
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la empreza: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = int(request.POST.get('estadoActivo'))
                    logo = request.FILES['file']
                    empresa = Empresa(descripcion=descripcion, estado=estadoActivo)
                    empresa.logo = logo
                    empresa.save()
                    mensaje = 'Empresa guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})

def UpdateEmpresa(request, *args, **kwargs):
    error = False
    mensaje = ''
    optionError = 0

    crud = int(request.POST.get('crud'))
    id = int(request.POST.get('id'))
    empresa = Empresa.objects.get(id=id)

    # ACTUALIZA EMPRESA
    if crud == 2:
        try:
            with transaction.atomic():
    
                descripcion = str(request.POST.get("descripcion")).upper()  # Leemos la descripción
    
                try:
                    Empresa.objects.exclude(id=id).get(descripcion=descripcion)
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la empresa: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0
    
                if optionError == 0:
                    empresa.descripcion = str(request.POST.get("descripcion")).upper()
                    empresa.estado = int(request.POST.get("estadoActivo"))
    
                    if "file" in request.FILES and request.FILES["file"]:
                        logo = request.FILES["file"]
                        empresa.logo = logo
    
                    empresa.save()
    
                mensaje = 'Empresa Actualizada'
        except Exception as e:
            error = True
            mensaje = str(e)
        return JsonResponse({'error': error, 'mensaje': mensaje, 'option':optionError})


    # ELIMINA UNA EMPRESA
    if crud == 3:
        try:
            with transaction.atomic():
                empresa.estado = -1
                empresa.save()
                mensaje = 'Empresa Eliminada'
        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje})


# *** BODEGAS ***#

class BodegasView(LoginRequiredMixin, TemplateView):
    template_name = 'public/bodegasView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bodegas'] = Bodega.objects.filter(Q(estado=1) | Q(estado=0))
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        optionError = 0  # 1: Existe empresa

        try:
            with transaction.atomic():
                nombre = str(request.POST.get('nombre')).upper()

                try:
                    Bodega.objects.get(nombre=nombre, estado__in=[0, 1])
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la bodega: ' + nombre
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = int(request.POST.get('estadoActivo'))
                    descripcion = str(request.POST.get('descripcion')).upper()
                    bodega = Bodega(nombre=nombre,descripcion=descripcion,estado=estadoActivo)
                    bodega.save()
                    mensaje = 'Bodega guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})

def UpdateBodega(request, *args, **kwargs):
    error = False
    mensaje = ''
    optionError = 0

    crud = int(request.POST.get('crud'))
    id = int(request.POST.get('id'))
    bodega = Bodega.objects.get(id=id)

    # ACTUALIZA Bodega
    if crud == 2:
        try:
            with transaction.atomic():

                nombre = str(request.POST.get("nombre")).upper()  # Leemos la descripción

                try:
                    Bodega.objects.exclude(id=id).get(nombre=nombre)
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la bodega: ' + nombre
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    bodega.nombre = str(request.POST.get("nombre")).upper()
                    bodega.descripcion = str(request.POST.get("descripcion")).upper()
                    bodega.estado = int(request.POST.get("estadoActivo"))
                    bodega.save()

                mensaje = 'Bodega Actualizada'
        except Exception as e:
            error = True
            mensaje = str(e)
        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})

    # ELIMINA UNA EMPRESA
    if crud == 3:
        try:
            with transaction.atomic():
                bodega.estado = -1
                bodega.save()
                mensaje = 'Bodega Eliminada'
        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje})


# *** ENTRADAS DE PIEZAS *** #

class EntradaPiezasView(LoginRequiredMixin, TemplateView):
    template_name = 'public/entradaPiezas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bodegas'] = Bodega.objects.filter(estado=1)
        context['piezasPrecios'] = PiezasPrecio.objects.select_related('pieza')
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        opcionError = 0  # 1: Existe usuario

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))

                try:
                    Piezas.objects.get(descripcion=descripcion)
                    optionError = 1
                    error = True
                    mensaje = 'Ya existe la pieza: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = bool(request.POST.get('estadoActivo'))
                    piezas = Piezas(descripcion=descripcion, estado=estadoActivo)
                    piezas.save()
                    mensaje = 'Pieza guardada correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': optionError})