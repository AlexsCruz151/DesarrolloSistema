from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView


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
