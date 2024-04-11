from django.shortcuts import render, redirect
from django.urls import reverse
from apps.accounts.forms import RegistrationForm

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
