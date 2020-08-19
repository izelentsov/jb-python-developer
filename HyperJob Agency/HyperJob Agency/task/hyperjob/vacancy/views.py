from django.views.generic.base import View
from django.shortcuts import render
from vacancy.models import Vacancy

# Create your views here.
class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vs = Vacancy.objects.all()
        context = { 'vs': vs }
        return render(request, 'vacancy/vacancies.html', context=context)
