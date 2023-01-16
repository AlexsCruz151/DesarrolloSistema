import requests
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class CategoriaView(LoginRequiredMixin, TemplateView):
    template_name = 'public/categoriaView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Home View'
        return context
