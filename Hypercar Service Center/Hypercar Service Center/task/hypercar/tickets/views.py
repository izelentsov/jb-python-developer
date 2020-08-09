from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http.response import HttpResponse


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html', context={})


class MenuView(TemplateView):
    template_name = 'tickets/menu.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
