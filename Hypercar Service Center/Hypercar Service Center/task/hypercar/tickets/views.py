from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from tickets.models import new_ticket, queue, SERV_DIAG, SERV_OIL, SERV_TIRES


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html', context={})


class MenuView(TemplateView):
    template_name = 'tickets/menu.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class GetTicketView(View):
    def get(self, request, serv_type, *args, **kwargs):
        serv_t = self.parse_serv_type(serv_type)
        ticket = new_ticket(serv_t)
        wait_time = queue.add(ticket)
        context = {
            't_num': ticket.id,
            'w_time': wait_time
        }
        return render(request, 'tickets/get_ticket.html', context=context)

    def parse_serv_type(self, serv_type_s):
        if serv_type_s == "change_oil":
            return SERV_OIL
        if serv_type_s == "inflate_tires":
            return SERV_TIRES
        if serv_type_s == "diagnostic":
            return SERV_DIAG
        return None


class ProcessingView(TemplateView):
    template_name = 'tickets/processing.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q_oil'] = queue.q_size(SERV_OIL)
        ctx['q_tires'] = queue.q_size(SERV_TIRES)
        ctx['q_diag'] = queue.q_size(SERV_DIAG)
        return ctx

    def post(self, request, *args, **kwargs):
        queue.choose_next()
        return redirect(to="/next")


class NextView(TemplateView):
    template_name = 'tickets/next.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        nt = queue.next_ticket()
        ctx['next_ticket'] = nt.id if nt is not None else None
        return ctx
