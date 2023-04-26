from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail , BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query_utils import Q
from django.contrib.auth.forms import PasswordResetForm

from django.http import HttpResponse

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
            password = request.POST['email']
            if not email.endswith('@ecs-co.com'):
                messages.error(request, 'Only email addresses from @ecs-co.com domain are allowed.' , extra_tags='error')
                return redirect('register')

            if Employee.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.', extra_tags='error')
                return redirect('register')

            Employee.objects.create(username = username, password = password , email = email)
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
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')
    

