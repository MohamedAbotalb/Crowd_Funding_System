from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('create/', views.create_project, name='create_project'),
    path('<str:title>', views.project_details, name='project_details'),
    path('<str:title>/rate', views.rate_project, name='rate_project'),
    path('<str:title>/donate', views.add_donations, name='add_donations'),
    path('<str:title>/update', views.update_project, name='update_project'),
    path('<str:title>/cancel',views.cancel_project,name='cancel_project'),
    path('<str:title>/comment', views.create_comment, name='create_comment'),
    path('<str:title>/report',views.report_project,name='report_project'),
    path('comments/<int:comment_id>/report',views.report_comment,name='report_comment'),
]
