import requests
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Home View'
        return context


class BaseJasperReport(object):
    report_name = ''
    module = ''
    format = ''
    filename = ''

    def __init__(self, report, module, format):
        self.auth = (settings.JASPER_USER, settings.JASPER_PASSWORD)
        self.report_name = report
        self.module = module
        self.format = format
        super(BaseJasperReport, self).__init__()

    def get_report(self):
        url = '{url}/rest_v2/reports/reports/{module}/{report_name}.{format}'.format(url=settings.JASPER_URL,
                                                                                     module=self.module,
                                                                                     report_name=self.report_name,
                                                                                     format=self.format)
        req = requests.get(url, params=self.get_params(), auth=self.auth)
        return req.content

    def get_params(self):
        """
        Este metodo sera implementado por cada uno de los reportes
        """
        raise NotImplementedError

    def render_to_response(self):
        if self.format == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.report_name)
        else:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(self.report_name)

        response.write(self.get_report())
        return response


class DownloadReport(BaseJasperReport):

    def __init__(self, data, modulo, reporte, formato):
        self.data = data
        super(DownloadReport, self).__init__(reporte, modulo, formato)

    def get_params(self):
        return self.data
