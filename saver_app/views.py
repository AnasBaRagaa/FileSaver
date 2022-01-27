import generics as generics
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from saver_app.forms import DataForm
from saver_app.models import Data


def index(request):
    return render(request, "saver_app/index.html")


def register(request):
    pass


def logout_user(request):
    logout(request)
    messages.info(request, "User logged out")
    return redirect('saver_app:index')


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


class CreateData(LoginRequiredMixin, generic.CreateView):
    success_message = "Data was added successfully."
    template_name = 'saver_app/create.html'
    success_url = reverse_lazy('saver_app:index')
    form_class = DataForm

    # send  current user to the form
    def get_form_kwargs(self):
        kwargs = super(CreateData, self).get_form_kwargs()
        print("user ", self.request.user.email)
        kwargs.update({'user': self.request.user})
        return kwargs

    # save the current user as the owner of the created record
    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        messages.success(self.request, self.success_message)
        return super(CreateData, self).form_valid(form)


def create_data_view(request):
    if request.user is None or not request.user.is_authenticated:
        messages.error(request,"No logged-in user")
        return render(request, 'registration/login.html')

    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        #form['owner'].value = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully")
            return reverse_lazy('saver_app:index')
        else:
            messages.error(request, "Invalid form")

    return render(request, 'saver_app/create.html', {'form': DataForm()})
