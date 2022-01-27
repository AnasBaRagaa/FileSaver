import generics as generics
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from saver_app.forms import DataForm
from saver_app.models import Data, SharingLink


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


class IndexClass(LoginRequiredMixin, generic.ListView):
    context_object_name = 'objects'

    def get_queryset(self, *args, **kwargs):
        qs = super(IndexClass, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)
        print('count =', qs.count)
        return qs

    model = Data
    template_name = "saver_app/index.html"


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    success_message = "Record was deleted successfully."
    template_name = 'saver_app/delete.html'  # Generic template
    model = Data
    success_url = reverse_lazy("saver_app:index")

    def get_object(self, queryset=None):
        obj = super(DeleteView, self).get_object()
        if obj.owner != self.request.user:
            # prevent users from deleting records they do not own
            raise Http404('You do not have permission to access this record')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)

        return super(DeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next', '') != '':
            # redirect back to the next page if this request was redirected from another page and has a next parameter
            self.request.session['data'] = self.request.POST
            return self.request.GET.get('next', '')
        return super(DeleteView, self).get_success_url()


class DetailView(LoginRequiredMixin, generic.DeleteView):
    context_object_name = "object"

    def get_object(self, queryset=None):
        obj = super(DetailView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404(
                'You do not have permission to access this record')  # prevent users from deleting records they do not own
        return obj

    model = Data
    template_name = 'saver_app/detail.html'


def create_sharing_link(request, pk):
    link = SharingLink(data_id=pk)
    link.save()
    return redirect(request.META.get('HTTP_REFERER'))


def public_link(request, pk):

    link = SharingLink.objects.filter(pk=pk)
    if link.count() == 1:
        return render(request, "saver_app/detail.html", {'object': link[0].data, 'public': True})
    else:
        raise Http404(
            'You do not have permission to access this record or link does not exist')


class DeleteLinkView(LoginRequiredMixin, generic.DeleteView):
    success_message = "Record was deleted successfully."
    template_name = 'saver_app/delete.html'  # Generic template
    model = SharingLink

    def get_object(self, queryset=None):
        obj = super(DeleteLinkView, self).get_object()
        if obj.data.owner != self.request.user:
            # prevent users from deleting records they do not own
            raise Http404('You do not have permission to access this record')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)

        return super(DeleteLinkView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('saver_app:details', kwargs={'pk': self.get_object().data.id})



