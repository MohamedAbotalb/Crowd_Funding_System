from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='accounts_activate'),
    path('home', views.home, name='home'),
    path("profile/", views.user_profile, name="profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("change_password/", views.change_password, name="change_password"),
    path("reset_password", views.password_reset_request, name="reset_password"),
    path('reset/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
]
