from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_index, name='category_index'),
    path('create/', views.category_create, name='category_create'),
    path('<slug:slug>/', views.category_show, name='category_show'),
    path('<slug:slug>/update/', views.category_update, name='category_update'),
    path('<slug:slug>/delete/', views.category_delete, name='category_delete'),
]