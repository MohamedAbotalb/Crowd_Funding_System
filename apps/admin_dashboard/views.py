from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django_countries import countries
from apps.projects.models import Project,ProjectPicture,Comment, Reply, Donation, CustomUser, Rating
import re
from apps.projects.forms import ProjectForm
from django.http import JsonResponse
from django_countries import countries
from apps.accounts.models import CustomUser
from apps.projects.models import Project, Donation, ProjectReport, CommentReport
from apps.categories.models import Category
from django.utils import timezone
from django.db.models import Avg, Max

def index(request):
    all_users_count = CustomUser.objects.all().count()
    all_projects_count = Project.objects.all().count()
    all_donations_count = Donation.objects.all().count()
    all_categories_count = Category.objects.all().count()

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
        'all_users_count': all_users_count,
        'all_projects_count': all_projects_count,
        'all_donations_count': all_donations_count,
        'all_categories_count': all_categories_count,
        'get_latest_users': get_latest_users,
        'get_latest_donations': get_latest_donations,
        'get_latest_projects': get_latest_projects,
        'get_featured_projects': get_featured_projects,
    }

    return render(request, 'admin_dashboard/index.html', context)

def show_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_dashboard/projects/project_list.html', {'projects': projects})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            project_pictures = request.FILES.getlist('pictures')
            tags = form.cleaned_data.get('tags', [])

            if len(project_pictures) == 0:
                messages.error(request, f'You should choose at least 1 picture.')
                return render(request, 'projects/create_project.html', {'form': form})

            if len(tags) > 5:
                form.add_error('tags', "Maximum 5 tags allowed.")
            for tag in tags:
                if not re.match(r'^[a-zA-Z0-9_]+$', tag):
                    form.add_error('tags', "Tags can only contain letters, numbers, and underscore.")
                    break
            if form.errors:
                return render(request, 'projects/create_project.html', {'form': form})

            project = form.save(commit=False)
            project.creator = user_instance
            project.save()
            form.save_m2m()

            for pic in project_pictures:
                ProjectPicture.objects.create(project=project, image=pic)

            return redirect('show_projects')
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})


def featured_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        # Toggle the featured status of the project
        project.featured = not project.featured
        project.save()
        return JsonResponse({'success': True, 'is_featured': project.featured})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def show_project(request, slug):
    # Fetch the project based on the provided slug
    project = get_object_or_404(Project, slug=slug)
    
    # Fetch comments and their replies for the project
    comments = Comment.objects.filter(project=project)
    
    
    # Calculate days left until end time
    end_datetime = project.end_time
    now_datetime = timezone.now()
    days_left = (end_datetime.date() - now_datetime.date()).days
    
    # Calculate the average rating for the project
    average_rating = project.ratings.aggregate(Avg('value'))['value__avg']
    if average_rating is not None:
        project.rate = round(average_rating, 2)
    else:
        project.rate = None
    project.save()
    
    # Retrieve the first and last donation made to the project
    first_donation = Donation.objects.filter(project=project).order_by('created_at').first()
    last_donation = Donation.objects.filter(project=project).order_by('-created_at').first()
    
    # Retrieve the top donation amount for the project
    top_donation = Donation.objects.filter(project=project).aggregate(Max('amount'))['amount__max']
    top_donation_user = CustomUser.objects.filter(donation__amount=Donation.objects.aggregate(max_amount=Max('amount'))['max_amount']).first()
    
    # Calculate the number of donors
    num_donors = Donation.objects.filter(project=project).values('user').distinct().count()
    
    context = {
        'project': project,
        'comments': comments,
        'days_left': days_left,
        'average_rating': average_rating,
        'first_donation': first_donation,
        'last_donation': last_donation,
        'top_donation': top_donation,
        'top_donation_user': top_donation_user,
        'num_donors': num_donors,
    }
    return render(request, 'admin_dashboard/projects/project_show.html', context)


def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        # Redirect to the admin dashboard index page after deletion
        return redirect('show_projects')
    return render(request, 'admin_dashboard/projects/project_list.html', {'project': project})

def delete_comment(request, slug, id):
    # Get the comment object
    comment = get_object_or_404(Comment, id=id)
    # Delete the comment
    comment.delete()
    # Redirect back to the project details page
    return redirect('show_project', slug=slug)
# return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)\
            

def show_reports(request):
    project_reports = ProjectReport.objects.all()
    comment_reports = CommentReport.objects.all()
    
    return render(request, 'admin_dashboard/reports/reports.html', {'project_reports': project_reports, 'comment_reports': comment_reports})

def show_comment_report(request, id):
    if id:
        comment_report = get_object_or_404(CommentReport, id=id)
    else:
        comment_report = CommentReport.objects.first()  
        
    return render(request, 'admin_dashboard/reports/comment_report.html', {'comment_report': comment_report})


def delete_comment_report(request, id):
    
    comment_report = get_object_or_404(CommentReport, id=id)
    comment_report.delete()
    
    return redirect('show_reports')


def show_project_report(request, id):
    
    if id:
        project_report = get_object_or_404(ProjectReport, id=id)
    else:
        project_report = ProjectReport.objects.first()
        
    return render(request, 'admin_dashboard/reports/project_report.html', {'project_report': project_report})


def delete_project_report(request, id):
    
    project_report = get_object_or_404(ProjectReport, id=id)
    project_report.delete()
    
    return redirect('show_reports')
