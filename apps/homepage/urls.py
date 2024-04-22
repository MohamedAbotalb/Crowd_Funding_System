from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
     path('api/projects/', views.get_projects_by_category_id, name='get_projects_by_category_id'),

]
