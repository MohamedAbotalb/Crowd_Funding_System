import re
from django.http import JsonResponse
from django.db.models import Avg, Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectPicture, Donation, Comment, ProjectReport, CommentReport
from .forms import ProjectForm, DonationForm, CommentForm, ReportProjectForm, ReportCommentForm
from apps.accounts.models import CustomUser
from .models import Project, Rating
from django.utils import timezone


# @login_required(login_url='login_')
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

def rate_project(request, slug):
    if request.method == 'POST':
        project = get_object_or_404(Project, slug=slug)
        print(project,"rate")
        rating_value = float(request.POST.get('rating'))
        print(rating_value,"rate")
        current_user = CustomUser.objects.get(pk=request.user.pk)
        # Check if the user has already rated the project
        existing_rating = Rating.objects.filter(user=current_user, project=project).first()
        if existing_rating:
            # Update existing rating
            existing_rating.value = rating_value
            existing_rating.save()
            messages.success(request, 'Your rating has been updated.')
        else:
            # Create a new rating object
            Rating.objects.create(user=current_user, project=project, value=rating_value)
            messages.success(request, 'Thank you for rating this project.')
        return JsonResponse({
            'success': True,
            'project_title': project.title,
            'project_slug': project.slug,
            'rating_value': rating_value,
             })
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # Calculate days left until end time
    end_datetime = project.end_time
    now_datetime = timezone.now()
    days_left = (end_datetime.date() - now_datetime.date()).days
    # Calculate the average rating for the project
    average_rating = project.ratings.aggregate(Avg('value'))['value__avg']
    print(average_rating,"avg")
    if average_rating is not None:
        project.rate = round(average_rating, 2)
        print(project.rate)
    else:
        project.rate = None
    project.save()
    # Check if the user has rated the project
    user_rating = None
    if request.user.is_authenticated:
        current_user = request.user
        user_rating_obj = Rating.objects.filter(user=current_user, project=project).first()
        if user_rating_obj:
            user_rating = user_rating_obj.value
    # Get related projects based on tags
    related_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id).distinct()[:4]
    # Calculate days left for each related project
    for related_project in related_projects:
            end_datetime = related_project.end_time
            now_datetime = timezone.now()
            days_left = (end_datetime.date() - now_datetime.date()).days
            related_project.days_left = days_left
    # Retrieve the first and last donation made to the project
    first_donation = Donation.objects.filter(project=project).order_by('created_at').first()
    last_donation = Donation.objects.filter(project=project).order_by('-created_at').first()
    # Retrieve the top donation amount for the project
    top_donation = Donation.objects.filter(project=project).aggregate(Max('amount'))['amount__max']
    top_donation_user = CustomUser.objects.filter(donation__amount=Donation.objects.aggregate(max_amount=Max('amount'))['max_amount']).first()
     # Calculate current fund percentage
    if project.total_target != 0:
        current_fund_percentage = round((project.current_fund / project.total_target) * 100, 2)
    else:
        current_fund_percentage = 0  # Handle division by zero case
    num_donors = Donation.objects.filter(project=project).values('user').distinct().count()
    print(request.user.id)
    print(project.creator.id)
    # Check if the user is the creator and current fund is less than 25% of target
    allow_cancel = False
    if request.user.id == project.creator.id and current_fund_percentage < 25:
        allow_cancel = True
        print(allow_cancel)
    context = {
        'project': project,
        'days_left': days_left,
        'user_rating': user_rating,
        'average_rating': average_rating,
        'related_projects': related_projects,
        'first_donation': first_donation,
        'last_donation': last_donation,
        'top_donation': top_donation,
        'top_donation_user': top_donation_user,
        'num_donors': num_donors,
        'current_fund_percentage': current_fund_percentage,
        'allow_cancel' : allow_cancel, 
    }
    return render(request, 'projects/project_details.html', context)

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


@login_required(login_url='login_')
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            report = CommentReport.objects.create(user=request.user, comment=comment, reason=reason)

            messages.success(request, "Thank you for reporting this comment. We will review it shortly.")

            return redirect('project_details', slug=comment.project.slug)
    else:
        form = ReportCommentForm()

    return render(request, 'projects/report_comment.html', {'form': form, 'comment': comment})
