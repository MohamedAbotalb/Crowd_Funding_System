import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from .models import Project, ProjectPicture, Donation, Comment, ProjectReport, CommentReport,Reply
from .forms import ProjectForm, DonationForm, CommentForm, ReportProjectForm, ReportCommentForm, ReplyCommentForm
from apps.accounts.models import CustomUser


@login_required(login_url='login_')
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

            return redirect('project_details', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})


def project_details(request, slug):
    project = Project.get_project_by_slug(slug)
    return render(request, 'projects/project_details.html', {'project': project})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    projects = Project.objects.filter(tags=tag)
    return render(request, '/projects/tagged.html', {'tag': tag, 'projects': projects})


@login_required(login_url='login_')
def cancel_project(request, slug):
    project = Project.get_project_by_slug(slug)
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

    project.delete()
    return redirect('/')

def add_donation(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            print(donation_form.cleaned_data['amount'])
            donation.project = project
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            donation.user = user_instance           
            donation.save()
            messages.success(request, 'Thank you for your donation!')
            return redirect('projects/project_details', slug=slug)
    else:
        donation_form = DonationForm()
    return render(request, 'projects/add_donation.html', {'donation_form': donation_form, 'project': project})

def add_comment(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            comment.user =  user_instance
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('projects/project_details', slug=slug)
    else:
        comment_form = CommentForm()
    return render(request, 'projects/add_comment.html', {'comment_form': comment_form, 'project': project})

def report_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        report_project_form = ReportProjectForm(request.POST)
        if report_project_form.is_valid():
            report = report_project_form.save(commit=False)
            report.project = project
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            report.user = user_instance
            report.save()
            messages.success(request, 'Thank you for reporting this project!')
            return redirect('projects/project_details', slug=slug)
    else:
        report_project_form = ReportProjectForm()
    return render(request, 'projects/report_project.html', {'report_project_form': report_project_form, 'project': project})

def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        report_comment_form = ReportCommentForm(request.POST)
        if report_comment_form.is_valid():
            report = report_comment_form.save(commit=False)
            report.comment = comment
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            report.user = user_instance
            report.save()
            messages.success(request, 'Thank you for reporting this comment!')
            return redirect('projects/project_details', slug=comment.project.slug)
    else:
        report_comment_form = ReportCommentForm()
    return render(request, 'projects/report_comment.html', {'report_comment_form': report_comment_form, 'comment': comment})