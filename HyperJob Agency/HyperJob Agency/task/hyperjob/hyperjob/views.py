from django.views.generic.base import TemplateView


class MenuView(TemplateView):
    template_name = 'hyperjob/menu.html'
