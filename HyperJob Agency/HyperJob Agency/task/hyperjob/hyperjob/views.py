from django.views.generic.base import View, TemplateView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.shortcuts import render
from resume.views import NewResumeForm
from vacancy.views import NewVacancyForm


class MenuView(TemplateView):
    template_name = 'hyperjob/menu.html'


class HyperSignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'hyperjob/signup.html'


class HyperLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'hyperjob/login.html'
    form_class = AuthenticationForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form, form_name, action = (NewVacancyForm(), "New Vacancy", "vacancy/new") \
            if request.user.is_staff \
            else (NewResumeForm(), "New Resume", "resume/new")
        ctx = {
            "new_form": form,
            "form_name": form_name,
            "action": action
        }
        return render(request, "hyperjob/home.html", context=ctx)
