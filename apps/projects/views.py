from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.accounts.models import CustomUser
from .models import Project, ProjectPicture
from .forms import ProjectForm
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
