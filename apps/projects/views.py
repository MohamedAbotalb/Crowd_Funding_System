from django.shortcuts import render, redirect

from .models import Project

# Create your views here.


def project_details(request, title):
    project = Project.get_project_by_title(title)
    return render(request, 'projects/project_details.html', {'project': project})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})
