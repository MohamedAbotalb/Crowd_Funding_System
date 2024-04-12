from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='accounts_activate'),
    path('home', views.home, name='home'),
    path("profile/",views.user_profile, name="profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
