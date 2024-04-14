from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_index, name='category_index'),
    path('create/', views.category_create, name='category_create'),
    path('<str:name>/', views.category_show, name='category_show'),
    path('<str:name>/update/', views.category_update, name='category_update'),
    path('<str:name>/delete/', views.category_delete, name='category_delete'),
]