from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, connection


class LoginView(TemplateView):
    template_name = 'usuarios/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            next_url = self.request.GET.get('next')
            if next_url is None:
                next_url = reverse_lazy('core:home')
            return HttpResponseRedirect(next_url)
        return super(LoginView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        status = HTTPStatus.OK
        if self.request.POST:
            form = AuthenticationForm(data=self.request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        login(self.request, user)
                        data = {'type': 'success', 'msg': 'Login Correcto'}
                    else:
                        data = {'type': 'error', 'msg': 'No tiene permiso para acceder'}
                        status = HTTPStatus.UNAUTHORIZED
                else:
                    data = {'type': 'error', 'msg': 'Credenciales Incorrectas'}
                    status = HTTPStatus.UNAUTHORIZED
            else:
                data = {'type': 'error', 'msg': 'Credenciales Incorrectas'}
                status = HTTPStatus.UNAUTHORIZED
        else:
            data = {'type': 'error', 'msg': 'Metodo no permitido'}
            status = HTTPStatus.METHOD_NOT_ALLOWED
        return JsonResponse(data=data, status=status)

class LogoutView(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            next_url = self.request.GET.get('next')
            if next_url is None:
                next_url = reverse_lazy('core:home')
            return HttpResponseRedirect(next_url)
        return super(LogoutView, self).dispatch(*args, **kwargs)

class ListView(TemplateView):
    template_name = 'usuarios/usuariosView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

def RegistrarUsuario(request,*args, **kwargs):
    error = False
    mensaje = ''
    opcionError = 0 # 1: Existe usuario

    try:
        with transaction.atomic():
            usuario = str(request.POST.get('usuario'))

            try:
                User.objects.get(username=usuario)
                optionError = 1
                error = True
                mensaje = 'Ya existe el usuario '+usuario
            except ObjectDoesNotExist:
                optionError = 0

            if optionError == 0:
                nombres = str(request.POST.get('nombres'))
                apellidos = str(request.POST.get('apellidos'))
                correo = str(request.POST.get('correo'))
                estadoSuperUsuario = bool(request.POST.get('estadoSuperUsuario'))
                estadoActivo = bool(request.POST.get('estadoActivo'))
                user = User.objects.create_user(username=usuario,first_name=nombres, last_name=apellidos,email=correo,is_superuser=estadoSuperUsuario,is_staff=True,is_active=estadoActivo)
                user.save()
                mensaje = 'Usuario guardado correctamente'
    except Exception as e:
        error = True
        mensaje = str(e)

    return JsonResponse({'error':error,'mensaje':mensaje,'option':optionError})
