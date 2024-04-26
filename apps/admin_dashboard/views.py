from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django_countries import countries
from apps.accounts.models import CustomUser
from apps.projects.models import Project, Donation, ProjectReport, CommentReport
from apps.categories.models import Category


def index(request):
    all_users = CustomUser.objects.all().count
    all_projects = Project.objects.all().count
    all_donations = Donation.objects.all().count()
    all_categories = Category.objects.all().count
    get_latest_users = CustomUser.objects.all().order_by('-date_joined')[:5]

    for user in get_latest_users:
        if user.country:
            country_name = dict(countries).get(user.country, user.country)
        else:
            country_name = None
        user.country = country_name

    get_latest_donations = Donation.objects.all().order_by('-created_at')[:5]
    get_latest_projects = Project.objects.filter(status='active').order_by('-start_time')[:5]
    get_featured_projects = Project.objects.filter(featured=True, status='active').order_by('-featured_at')[:5]

    context = {
        'all_users': all_users,
        'all_projects': all_projects,
        'all_donations': all_donations,
        'all_categories': all_categories,
        'get_latest_users': get_latest_users,
        'get_latest_donations': get_latest_donations,
        'get_latest_projects': get_latest_projects,
        'get_featured_projects': get_featured_projects,
    }

    return render(request, 'admin_dashboard/index.html', context)

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
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)\
            

def show_reports(request):

    project_reports = ProjectReport.objects.all()
    comment_reports = CommentReport.objects.all()
    
    return render(request, 'admin_dashboard/reports.html', {'project_reports': project_reports, 'comment_reports': comment_reports})


def show_comment_report(request, id=None):
    if id:
        comment_report = get_object_or_404(CommentReport, id=id)
    else:
        comment_report = CommentReport.objects.first()  
        
    return render(request, 'admin_dashboard/show_comment_report.html', {'comment_report': comment_report})


def delete_comment_report(request, id):
    
    comment_report = get_object_or_404(CommentReport, id=id)
    comment_report.delete()

    return redirect('show_comment_report')


def show_project_report(request, id=None):
    
    if id:
        project_report = get_object_or_404(ProjectReport, id=id)
    else:
        project_report = ProjectReport.objects.first()
        
    return render(request, 'admin_dashboard/show_project_report.html', {'project_report': project_report})


def delete_project_report(request, id):
    
    project_report = get_object_or_404(ProjectReport, id=id)
    project_report.delete()
    
    return redirect('show_project_report')
