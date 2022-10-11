from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from apps.hubstaffapihelper import login as hubstaff_login

# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    
    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(email, password)
            #user = authenticate(username=username, password=password)

            hub_response = hubstaff_login(email, password)
            print("hubstaff response",  hub_response)

            if hub_response.status_code == 200:
                request.session[settings.AUTH_TOKEN] = hub_response.json()["auth_token"]
                user, created = User.objects.get_or_create(username = email)
                login(request, user)
                print("login succeed sessioin view", request.session[settings.AUTH_TOKEN])
                return redirect("/")
            else :
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
   

    return render(request, "login.html", {"form": form, "msg": msg})

def logout_view(request):
    return redirect("login/")