from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404
from apps.accounts.models import CustomUser
from .models import Project, ProjectPicture, Donation, Comment, ProjectReport
from .forms import ProjectForm, DonationForm, CommentForm, ReportProjectForm
# Create your views here.


@login_required(login_url='login_')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            user_instance = CustomUser.objects.get(pk=request.user.pk)
            tags = form.cleaned_data.get('tags', [])
            if len(tags) > 5:
                form.add_error('tags', "Maximum 5 tags allowed.")
            for tag in tags:
                if not tag.startswith('#'):
                    form.add_error('tags', "Tags must start with '#' character.")
            if form.errors:
                return render(request, 'projects/create.html', {'form': form})

            project_pictures = request.FILES.getlist('pictures')
            if len(project_pictures) == 0:
                messages.error(request, f'You should choose at least 1 picture.')
                return render(request, 'projects/create.html', {'form': form})

            project = form.save(commit=False)
            project.creator = user_instance
            project.save()

            for pic in project_pictures:
                ProjectPicture.objects.create(project=project, image=pic)

            return redirect('project_details', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})


def project_details(request, slug):
    project = Project.get_project_by_slug(slug)
    return render(request, 'projects/project_details.html', {'project': project})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})

@login_required(login_url='login_')
def add_donations(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            if amount <= 0:
                messages.error(request, "Donation amount should be greater than zero.")
                return redirect('project_details', slug=slug)
            
            if project.status == 'completed':
                messages.error(request, "This project has already been completed.")
                return redirect('project_details', slug=slug)
            
            if project.status == 'active' and project.current_fund + amount > project.total_target:
                messages.error(request, "The donation amount exceeds the total target of the project.")
                return redirect('project_details', slug=slug)
            
            # Create a new donation object
            donation = Donation.objects.create(amount=amount, project=project, user=request.user)
            
            # Update the current fund of the project
            project.current_fund += amount
            project.save()
            
            messages.success(request, f"Thank you for your donation!")
            
            return redirect('project_details', slug=slug)
    else:
        form = DonationForm()
    
    return render(request, 'projects/add_donation.html', {'form': form, 'project': project})

@login_required(login_url='login_')
def create_comment(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            
            # Create a new comment object
            comment = Comment.objects.create(user=request.user, project=project, text=comment_text)
            
            messages.success(request, "Your comment has been added successfully!")
            
            return redirect('project_details', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, 'projects/create_comment.html', {'form': form, 'project': project})

@login_required(login_url='login_')
def report_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ReportProjectForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            # Create a new project report object
            report = ProjectReport.objects.create(user=request.user, project=project, reason=reason)
            
            messages.success(request, "Thank you for reporting this project. We will review it shortly.")
            
            return redirect('project_details', slug=slug)
    else:
        form = ReportProjectForm()
    
    return render(request, 'projects/report_project.html', {'form': form, 'project': project})