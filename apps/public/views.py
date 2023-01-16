import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from ..public.models import Categoria
from django.db import transaction, connection
from django.http import HttpResponseNotFound, JsonResponse


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
