from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
