import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from .models import Project, ProjectPicture, Donation, Comment, ProjectReport, CommentReport,Reply
from .forms import ProjectForm, DonationForm, CommentForm, ReportProjectForm, ReportCommentForm, ReplyCommentForm
from apps.accounts.models import CustomUser
from django.http import JsonResponse
from django.db.models import F


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

@login_required(login_url='login_')
def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    comments = project.comments.all()
    donation_form = DonationForm()
    comment_form = CommentForm()
    report_project_form = ReportProjectForm()
    report_comment_form = ReportCommentForm()
    reply_comment_form = ReplyCommentForm()

    if request.method == 'POST':
        if 'donate_button' in request.POST:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.project = project
                donation.user = request.user
                donation.save()
                project.current_fund = F('current_fund') + donation.amount
                project.save()
                messages.success(request, 'Thank you for your donation!')
                return redirect('project_details', slug=slug)
        elif 'report_project_button' in request.POST:
            report_project_form = ReportProjectForm(request.POST)
            if report_project_form.is_valid():
                report = report_project_form.save(commit=False)
                report.project = project
                report.user = request.user
                report.save()
                messages.success(request, 'Project reported successfully!')
                return redirect('project_details', slug=slug)
        elif 'comment_button' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('project_details', slug=slug)
        elif 'report_comment_button' in request.POST:
            report_comment_form = ReportCommentForm(request.POST)
            if report_comment_form.is_valid():
                report = report_comment_form.save(commit=False)
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                report.comment = comment
                report.user = request.user
                report.save()
                messages.success(request, 'Comment reported successfully!')
                return redirect('project_details', slug=slug)
        elif 'reply_comment_button' in request.POST:
            reply_comment_form = ReplyCommentForm(request.POST)
            if reply_comment_form.is_valid():
                reply = reply_comment_form.save(commit=False)
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                reply.project = project
                reply.user = request.user
                reply.parent = comment
                reply.save()
                messages.success(request, 'Reply added successfully!')
                return redirect('project_details', slug=slug)

    return render(request, 'projects/project_details.html', {'project': project, 'comments': comments, 'donation_form': donation_form, 'comment_form': comment_form, 'report_project_form': report_project_form, 'report_comment_form': report_comment_form, 'reply_comment_form': reply_comment_form})