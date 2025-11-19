from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'main/index.html'


class TranscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'
