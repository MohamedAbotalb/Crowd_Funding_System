from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user, name='accounts_register'),
    path('activate/<uidb64>/<token>', views.activate, name='accounts_activate'),
]
