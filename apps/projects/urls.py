from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('create/', views.create_project, name='create_project'),
    path('project/<slug:slug>/', views.project_details, name='project_details'),
    path('<slug:slug>/rate', views.rate_project, name='rate_project'),
    path('<slug:slug>/cancel/', views.cancel_project, name='cancel_project'),
    path('tags/<slug:slug>/', views.tagged, name="tagged"),
]