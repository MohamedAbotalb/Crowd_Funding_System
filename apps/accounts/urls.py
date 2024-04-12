from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path('logout', views.logout_user, name='logout'),
    path('profile/',views.profile_page, name='accounts_profile'),
    path('activate/<uidb64>/<token>', views.activate, name='accounts_activate'),
    path('home', views.home, name='home')
]
