import os
import shutil

from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, Avg, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django_countries import countries

from .decorators import superuser_required
from apps.projects.forms import ProjectForm
from apps.accounts.models import CustomUser
from apps.projects.models import Project, Donation, ProjectPicture, Comment, ProjectReport, CommentReport, Reply, Rating
from apps.categories.models import Category
from apps.categories.forms import CategoryForm


@superuser_required
def index(request):
    all_users = CustomUser.objects.all().count()
    all_projects = Project.objects.all().count()
    all_donations = Donation.objects.all().count()
    all_categories = Category.objects.all().count()
    get_latest_users = CustomUser.objects.all().order_by('-date_joined')[:5]

    for user in get_latest_users:
        if user.country:
            country_name = dict(countries).get(user.country, user.country)
        else:
            country_name = 'None'
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


@superuser_required
def show_users(request):
    all_users = CustomUser.objects.all().order_by('-date_joined')

    for user in all_users:
        if user.country:
            country_name = dict(countries).get(user.country, user.country)
        else:
            country_name = 'None'
        user.country = country_name

    return render(request, 'admin_dashboard/users/index.html', {'all_users': all_users})


@superuser_required
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.delete()
    return redirect('show_users')


@superuser_required
def show_donations(request):
    all_donations = Donation.objects.all().order_by('-created_at')
    total_donations = Donation.objects.aggregate(total_donations=Sum('amount'))['total_donations']

    context = {
        'all_donations': all_donations,
        'total_donations': total_donations,
    }

    return render(request, 'admin_dashboard/donations/index.html', context)


@superuser_required
def show_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_dashboard/projects/project_list.html', {'projects': projects})


@superuser_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project_pictures = request.FILES.getlist('image')
            print(project_pictures)
            for pic in project_pictures:
                ProjectPicture.objects.create(project=project, image=pic)
            project.save()
            return redirect('show_project', slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'admin_dashboard/projects/edit_project.html', {'form': form, 'project': project})


@superuser_required
def project_picture(request, slug):
    project = get_object_or_404(Project, slug=slug)
    print(slug,"slug")
    project_pictures = ProjectPicture.objects.filter(project__slug=slug)
    return render(request, 'admin_dashboard/projects/project_pictures.html', {'project': project,'pictures': project_pictures})


@superuser_required
def delete_project_picture(request,slug, pk):
    project_picture = get_object_or_404(ProjectPicture, pk=pk)
    print(slug,"slug")
    if request.method == 'POST':
        project_picture.delete()
    return redirect(reverse('project_picture', kwargs={'slug': slug}))


@superuser_required
def featured_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.featured = not project.featured
        project.save()
        return JsonResponse({'success': True, 'is_featured': project.featured})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@superuser_required
def show_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    comments = Comment.objects.filter(project=project)
    end_datetime = project.end_time
    now_datetime = timezone.now()
    days_left = (end_datetime.date() - now_datetime.date()).days
    average_rating = project.ratings.aggregate(Avg('value'))['value__avg']
    if average_rating is not None:
        project.rate = round(average_rating, 2)
    else:
        project.rate = None
    project.save()
    first_donation = Donation.objects.filter(project=project).order_by('created_at').first()
    last_donation = Donation.objects.filter(project=project).order_by('-created_at').first()
    top_donation = Donation.objects.filter(project=project).aggregate(Max('amount'))['amount__max']
    top_donation_user = CustomUser.objects.filter(donation__amount=Donation.objects.aggregate(max_amount=Max('amount'))['max_amount']).first()
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


@superuser_required
def delete_project(request, slug):
    project = Project.get_project_by_slug(slug)
    if request.method == 'POST':
        project_directory = os.path.join(settings.MEDIA_ROOT, 'project_uploads', project.title.replace(' ', '_'))
        current_fund = project.current_fund
        recipient_project = Project.objects.filter(category=project.category).exclude(pk=project.pk).first()

        # add the current fund of that project to another project in the same category
        if recipient_project:
            recipient_project.current_fund += current_fund
            recipient_project.save()

        else:
            # If no project in the same category, transfer the funds to any available project
            recipient_project = Project.objects.exclude(pk=project.pk).first()
            recipient_project.current_fund += current_fund
            recipient_project.save()

        # Delete the project directory
        if os.path.exists(project_directory):
            shutil.rmtree(project_directory)

        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('show_projects')

    return render(request, 'admin_dashboard/projects/project_list.html', {'project': project})


@superuser_required
def delete_comment(request, slug, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('show_project', slug=slug)


@superuser_required
def show_reports(request):
    project_reports = ProjectReport.objects.all()
    comment_reports = CommentReport.objects.all()

    return render(request, 'admin_dashboard/reports/reports.html', {'project_reports': project_reports, 'comment_reports': comment_reports})


@superuser_required
def show_comment_report(request, id):
    if id:
        comment_report = get_object_or_404(CommentReport, id=id)
    else:
        comment_report = CommentReport.objects.first()

    return render(request, 'admin_dashboard/reports/comment_report.html', {'comment_report': comment_report})


@superuser_required
def delete_comment_report(request, id):
    comment_report = get_object_or_404(CommentReport, id=id)
    comment_report.delete()

    return redirect('show_reports')


@superuser_required
def show_project_report(request, id):
    if id:
        project_report = get_object_or_404(ProjectReport, id=id)
    else:
        project_report = ProjectReport.objects.first()

    return render(request, 'admin_dashboard/reports/project_report.html', {'project_report': project_report})


@superuser_required
def delete_project_report(request, id):
    project_report = get_object_or_404(ProjectReport, id=id)
    project_report.delete()

    return redirect('show_reports')


@superuser_required
def show_categories(request):
    all_categories = Category.get_all_categories()
    return render(request, 'admin_dashboard/categories/show_categories.html', {'all_categories': all_categories})


@superuser_required
def show_category(request, slug):
    category = Category.get_category_by_slug(slug)
    Projects = Project.objects.all().filter(category_id=category.id)
    return render(request, 'admin_dashboard/categories/show_category.html', {'category': category, 'Projects': Projects})


@superuser_required
def create_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect(category.show_url)
    return render(request, 'admin_dashboard/categories/create_categories.html', {'form': form})


@superuser_required
def update_category(request, slug):
    category = Category.get_category_by_slug(slug)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(category.show_url)
    return render(request, 'admin_dashboard/categories/update_categories.html', context={"form": form})


@superuser_required
def delete_category(request, slug):
    category = Category.get_category_by_slug(slug)
    category.delete()
    return redirect('show_categories')
