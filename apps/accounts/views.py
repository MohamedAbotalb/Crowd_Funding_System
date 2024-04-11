from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from apps.accounts.forms import RegistrationForm
from apps.accounts.models import CustomUser
from django.contrib.auth.models import User 
from django.contrib.auth import get_user

# Create your views here.
def create_user(request):
    form = RegistrationForm()
    # if request.user.is_authenticated: 
    #     return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_url = reverse("login")
            return redirect(login_url)
    return render(request, 'registration/register.html', {'form':form})

from django.contrib.auth import authenticate, login

# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect('/')  # Redirect if user is already logged in

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             # Add an error message to be displayed in the template
#             messages.error(request, 'Invalid username or password')

#     return render(request, 'login.html')


def user_profile(request):
    User = get_user(request)
    print(User.id)
    user_data = get_object_or_404(CustomUser, pk=2)
    User.phone_number = user_data.phone_number
    User.profile_picture = user_data.profile_picture
    User.facebook_profile = user_data.facebook_profile
    User.birth_date = user_data.birth_date
    User.country = user_data.country
    print(User)

    return render(request, "profile/profile_page.html",
                  context={"User": User})  

