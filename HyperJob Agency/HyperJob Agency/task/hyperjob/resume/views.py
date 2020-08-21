from django.shortcuts import render, redirect
from django.views.generic.base import View
from resume.models import Resume
from django import forms
from django.http.response import HttpResponseForbidden, Http404


# Create your views here.
class ResumesView(View):
    def get(self, request, *args, **kwargs):
        rs = Resume.objects.all()
        context = { 'rs': rs }
        return render(request, 'resume/resumes.html', context=context)


class NewResumeForm(forms.Form):
    description = forms.CharField(max_length=1024)


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = NewResumeForm(request.POST)
        if form.is_valid():
            desc = form.cleaned_data['description']
            Resume.objects.create(description=desc, author=request.user)
            return redirect(to="/home")
        return Http404
