from biodb import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from mixins import LoginRequiredMixin
from django.views import generic
from models import Project


# Create your views here.
def redirect_to_home(request):
    ''' In case of request '/' redirect to '/projects/' '''  
    return redirect(to=settings.HOME_URL)

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'projects/projects.html'
    model = Project
