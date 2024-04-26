from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from apps.accounts.models import CustomUser
from apps.projects.models import Project, Donation
from apps.categories.models import Category


def index(request):
    all_users = CustomUser.objects.all().count()
    all_projects = Project.objects.all().count()
    all_donations = Donation.objects.all().count()
    all_categories = Category.objects.all().count()
    return render(request, 'admin_dashboard/index.html', {'all_users': all_users, 'all_projects': all_projects,
                                                          'all_donations': all_donations, 'all_categories': all_categories})

def show_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_dashboard/projects/project_list.html', {'projects': projects})

def featured_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        # Toggle the featured status of the project
        project.featured = not project.featured
        project.save()
        return JsonResponse({'success': True, 'is_featured': project.featured})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)