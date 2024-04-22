from django.shortcuts import render,get_object_or_404
from django.db.models import Avg, Count
from django.utils import timezone
from django.http import JsonResponse
from apps.projects.models import Project
from apps.categories.models import Category
from apps.accounts.models import CustomUser
# Create your views here.



def home_page(request):
    top_projects = Project.objects.filter(status='active', end_time__gt=timezone.now()).order_by('-rate')[:5]
    categories = Category.objects.all()
    categories_projects=Project.objects.all()
    for project in categories_projects:
        percentage = project.current_fund * 100 / project.total_target
        project.percentage = percentage

    latest_projects = Project.objects.order_by('-start_time')[:5]
    for project in latest_projects:
        percentage = project.current_fund * 100 / project.total_target
        project.percentage = percentage

    featured_projects = Project.objects.filter(featured=True).order_by('-featured_at')[:5]
    for project in featured_projects:
        percentage = project.current_fund * 100 / project.total_target
        project.percentage = percentage

    return render(request, 'homepage/index.html',context = {'top_projects':top_projects,
                                                            'latest_projects': latest_projects,
                                                            'featured_projects':featured_projects,
                                                            'categories':categories,
                                                            'categories_projects':categories_projects,
                                                            })

def get_projects_by_category_id(request):
    category_id = request.GET.get('category_id')
    if category_id:
        projects = Project.objects.filter(category_id=category_id)
    else:
        projects = Project.objects.all()

    data = [{'id': project.id, 'title': project.title, 'details': project.details, 
             'picture_url': project.picture_url, 'current_fund': project.current_fund, 
             'total_target': project.total_target} 
            for project in projects]

    return JsonResponse({'projects': data})
    



 
    


