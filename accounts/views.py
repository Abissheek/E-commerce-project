from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#account verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0] 
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            #user activation
            current_site=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),


            })
            to_email=email
            send_email=EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()
          #  messages.success(request, 'Registration Successfull. We have sent a verification link to your email. Please varify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm() 
    context={
        'form':form
    }
    return render(request, 'register.html', context)



def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)


        if user is not None:
            auth.login(request,user)
           # messages.success(request,'You are logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email and password')
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url ='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logout.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'Congratulation! Your account activated')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')