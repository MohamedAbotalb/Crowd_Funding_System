from django.shortcuts import render
from django.http import HttpResponse

from apps.accounts.models import CustomUser
from apps.projects.models import Project, Donation
from apps.categories.models import Category


def index(request):
    all_users = CustomUser.objects.all().count
    all_projects = Project.objects.all().count
    all_donations = Donation.objects.all().count
    all_categories = Category.objects.all().count
    return render(request, 'admin_dashboard/index.html', {'all_users': all_users, 'all_projects': all_projects,
                                                          'all_donations': all_donations, 'all_categories': all_categories})
