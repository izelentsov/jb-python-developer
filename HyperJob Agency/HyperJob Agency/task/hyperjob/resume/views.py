from django.shortcuts import render
from django.views.generic.base import View
from resume.models import Resume

# Create your views here.
class ResumesView(View):
    def get(self, request, *args, **kwargs):
        rs = Resume.objects.all()
        context = { 'rs': rs }
        return render(request, 'resume/resumes.html', context=context)
