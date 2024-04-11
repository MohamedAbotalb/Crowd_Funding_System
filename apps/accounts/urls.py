from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path("profile",views.user_profile, name="profile")

]
