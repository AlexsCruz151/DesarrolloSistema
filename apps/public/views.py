import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from ..public.models import Categoria, Piezas, Empresa, Bodega, PiezasPrecio, EntradaPiezas, DetalleEntradaPiezas, Productos, Productospiezas
from django.db import transaction, connection
from django.http import HttpResponseNotFound, JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
import json
import decimal
from django.db.models import F
#g

#*** CATEGORÍA ***#

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

#*** FIN DE CATEGORÍA ***#





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
                id_usuario = request.user.id

                try:
                    Piezas.objects.get(Q(descripcion=descripcion) | Q(codigo=codigoReferencia),estado__in=[0,1])
                    opcionError = 1
                    error = True
                    mensaje = 'Ya existe la pieza: ' + descripcion
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = int(request.POST.get('estadoActivo'))
                    piezas = Piezas(codigo=codigoReferencia, descripcion=descripcion, estado=estadoActivo,usuario_grabacion_id=id_usuario)
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
    id_usuario = request.user.id

    try:
        with transaction.atomic():
            piezas.descripcion = str(request.POST.get("descripcion"))
            piezas.estado = bool(request.POST.get("estadoActivo"))
            piezas.usuario_modificacion_id = id_usuario
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
        context['piezas'] = Piezas.objects.filter(estado=1)
        context['entradasPiezas'] = EntradaPiezas.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Guarda EntradasPiezas
        # Guarda DetalleEntradaPiezas
        # Atualiza PiezasPrecio

        error = False
        mensaje = '¡Entrada de piezas registrada!'
        idEntradaPieza = 0

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))
                id_bodega = int(request.POST.get('id_bodega'))
                estado = int(request.POST.get('estadoActivo'))
                data = json.loads(request.POST.get('entradas'))

                try:
                    entradaPieza = EntradaPiezas()
                    entradaPieza.descripcion = descripcion
                    entradaPieza.save()
                    id_entrada_pieza = entradaPieza.id

                    for datos in data:

                        id_pieza = int(datos[0])
                        cantidad = int(datos[2])
                        precio = float(datos[3])

                        existe_precio = PiezasPrecio.objects.filter(precio=precio,bodega__id=id_bodega)

                        if existe_precio.exists():
                            PiezasPrecio.objects.filter(piezas__id=id_pieza,bodega__id=id_bodega).update(cantidad=F('cantidad') + cantidad)
                        else:
                            piezasPrecio = PiezasPrecio(pieza_id=id_pieza,cantidad=cantidad,precio=precio,bodega_id=id_bodega)
                            piezasPrecio.save()
                            id_piezas_precio = piezasPrecio.id

                            detalleEntradaPiezas = DetalleEntradaPiezas(pieza_precio_id=id_piezas_precio,entrada_pieza_id=id_entrada_pieza,cantidad=cantidad)
                            detalleEntradaPiezas.save()


                except Exception as e:
                    error = False
                    mensaje = 'Error al guardar en Entrada Pieza: '+e

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje})


def GetDetalleEntrada(request, *args, **kwargs):

    id_entrada = int(request.POST.get('id_entrada'))

    detalle_piezas = DetalleEntradaPiezas.objects.select_related('pieza_precio__pieza','pieza_precio__bodega').filter(entrada_pieza_id=id_entrada)
    data = []

    for detalle in detalle_piezas:
        data.append({
            'piezas_id': detalle.pieza_precio.pieza.id,
            'nombre_pieza': detalle.pieza_precio.pieza.descripcion,
            'cantidad': detalle.cantidad,
            'precio': detalle.pieza_precio.precio,
            'nombre_bodega': detalle.pieza_precio.bodega.nombre
        })

    return JsonResponse(list(data),safe=False)





# *** PRODUCTOS *** #

class ProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'public/productosView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Productos.objects.filter(estado=1)
        return context

    def post(self, request, *args, **kwargs):
        error = False
        mensaje = ''
        opcionError = 0  # 1: Existe descripcion o codigo

        try:
            with transaction.atomic():
                descripcion = str(request.POST.get('descripcion'))
                codigoReferencia = str(request.POST.get('codigo'))
                cantidad = int(request.POST.get('cantidad'))
                precio = float(request.POST.get('precio'))
                tipo = int(request.POST.get('tipo'))
                id_usuario = request.user.id

                try:
                    Productos.objects.get(Q(descripcion=descripcion) | Q(codigo=codigoReferencia),estado__in=[0,1])
                    opcionError = 1
                    error = True
                    mensaje = 'Ya existe la producto con la misma descripción o el mismo código de referencia'
                except ObjectDoesNotExist:
                    optionError = 0

                if optionError == 0:
                    estadoActivo = int(request.POST.get('estadoActivo'))
                    producto = Productos(codigo=codigoReferencia, descripcion=descripcion, estado=estadoActivo,usuario_grabacion_id=id_usuario,cantidad=cantidad,precio=precio, tipo=tipo)
                    imagen = request.FILES['file']
                    producto.imagen = imagen
                    producto.save()
                    mensaje = 'Producto guardado correctamente'

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje, 'option': opcionError})

def UpdateProducto(request, *args, **kwargs):
    error = False
    mensaje = ''

    id = str(request.POST.get('id'))
    piezas = Piezas.objects.get(id=id)
    id_usuario = request.user.id

    try:
        with transaction.atomic():
            piezas.descripcion = str(request.POST.get("descripcion"))
            piezas.estado = bool(request.POST.get("estadoActivo"))
            piezas.usuario_modificacion_id = id_usuario
            piezas.save()
            mensaje = 'Pieza Actualizada'

    except Exception as e:
        error = True
        mensaje = str(e)

    return JsonResponse({'error': error, 'mensaje': mensaje})

def GetProducto(request, *args, **kwargs):

    get = int(request.POST.get('get'))

    if get == 1: # Extraer detalle de precios
        detalle_precios = PiezasPrecio.objects.filter(pieza__id=1)
        return JsonResponse(list(detalle_precios),safe=False)





# *** MANOFACTURA DE PRODUCTOS *** #

class ManofacturaProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'public/manofacturaProductosView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Productos.objects.filter(estado=1,tipo=1)
        context['piezas'] = Piezas.objects.filter(estado=1)
        return context

    def post(self, request, *args, **kwargs):
        # Guarda EntradasPiezas
        # Guarda DetalleEntradaPiezas
        # Atualiza PiezasPrecio

        error = False
        mensaje = '¡Piezas de productos registrada!'
        idEntradaPieza = 0
        existePieza = False

        try:
            with transaction.atomic():
                id_producto = int(request.POST.get('id_producto'))
                data = json.loads(request.POST.get('piezas'))

                try:
                    for datos in data:

                        id_pieza = int(datos[0])
                        id_producto = int(id_producto)
                        cantidad = int(datos[3])

                        existe = Productospiezas.objects.filter(producto__id=id_producto,pieza__id=id_pieza, estado=1).exists()

                        if existe:
                            existePieza = True
                        else:
                            productosPiezas = Productospiezas(pieza_id=id_pieza,producto_id=id_producto,cantidad=cantidad)
                            productosPiezas.save()

                except Exception as e:
                    error = False
                    mensaje = 'Error al guardar Detalle de pieza: '+str(e)

        except Exception as e:
            error = True
            mensaje = str(e)

        return JsonResponse({'error': error, 'mensaje': mensaje})

def UpdateManofacturaProductos(request, *args, **kwargs):
    error = False
    mensaje = ''

    #1: Eliminar pieza del detalle
    update = int(request.POST.get('update'))

    if update == 1:
        codigoPieza = int(request.POST.get('codigo'))
        id_producto = int(request.POST.get('id_producto'))

        try:
            existe = Productospiezas.objects.filter(producto__id=id_producto,pieza__id=codigoPieza).exists()

            if existe:
                productoPieza = Productospiezas.objects.get(producto__id=id_producto,pieza__id=codigoPieza)
                productoPieza.estado = -1
                productoPieza.save()

        except Exception as e:
            error = True

        return JsonResponse({'error':error,'mensaje':"Actualizado con éxito"})


def GetManofacturaProductos(request, *args, **kwargs):

    get = int(request.POST.get('get'))

    if get == 1: # Extraer detalle piezas

        id_producto = request.POST.get('id_producto')

        detallePiezas = Productospiezas.objects.select_related('pieza','producto').filter(producto_id=id_producto,estado__in=[1])
        data = []

        for detalle in detallePiezas:
            data.append({
                'id_pieza': detalle.pieza.id,
                'codigo': detalle.pieza.codigo,
                'nombre': detalle.pieza.descripcion,
                'cantidad': detalle.cantidad
            })

        return JsonResponse(list(data),safe=False)
