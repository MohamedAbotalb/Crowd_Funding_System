from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path("profile/",views.user_profile, name="profile"),
    path('activate/<uidb64>/<token>', views.activate, name='accounts_activate'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
