from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.http.response import HttpResponseForbidden, Http404
from vacancy.models import Vacancy
from django import forms

# Create your views here.
class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vs = Vacancy.objects.all()
        context = { 'vs': vs }
        return render(request, 'vacancy/vacancies.html', context=context)


class NewVacancyForm(forms.Form):
    description = forms.CharField(max_length=1024)


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden()
        form = NewVacancyForm(request.POST)
        if form.is_valid():
            desc = form.cleaned_data['description']
            Vacancy.objects.create(description=desc, author=request.user)
            return redirect(to="/home")
        return Http404

