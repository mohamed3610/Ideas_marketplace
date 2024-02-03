from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from Ideas.models import Ideas
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    
    
    
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('register')

def register(request):
    if request.method == 'POST':
       
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            department = request.POST['department']
            if not email.endswith('@ecs-co.com'):
                messages.error(request, 'Only email addresses from @ecs-co.com domain are allowed.' , extra_tags='error')
                return redirect('register')

            if Employee.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.', extra_tags='error')
                return redirect('register')

            Employee.objects.create_user(username = username, password = password , email = email , 
                                         first_name = first_name , last_name = last_name , department = department)
            messages.success(request, f'Account created for {username}! they can now login.')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')
    



def login_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')
    


def homePage(request):
    if request.user.is_authenticated:
        ideas = Ideas.objects.all()[:4]
        return render(request , "authentication/home.html" , {"ideas": ideas})
    else:
        return redirect("register")

def logout_employee(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have loged out')
        return redirect("register")
    else:
         return redirect("register")

