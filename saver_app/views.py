import generics as generics
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic


# Create your views here.
def index(request):
    return HttpResponse("Index page")


def register(request):
    pass


def logout_user(request):
    pass


def auth(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email__iexact=email).first()
        if user is not None and user.check_password(password):

            login(request, user)
            messages.success(request, 'Successful Login')
            return redirect("saver_app:index")

        else:

            messages.error(request, 'Unsuccessful Login')

    return render(request, 'registration/login.html')
