from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def register(request):
    """ Register a new user. """
    if request.method != 'POST':
        # Diaplay blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data = request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('learning_logs:index')
        
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)



class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name = 'registration/profile_creation.html'
    fields = ['user', 'image', 'rol']   

    def form_valid(self, form):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            return redirect('users:profile-detail')
        except UserProfile.DoesNotExist:
            form.instance.user = self.request.user
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile-detail', kwargs={'pk': self.object.pk})
    
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'registration/profile_detail.html'
    context_object_name = 'userprofile'
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'registration/profile_update.html'
    fields = ['image', 'rol']

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('users:profile-detail', kwargs={'pk': self.object.user.profile.pk})

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'registration/profile_delete.html'

    def get_success_url(self):
        return reverse_lazy('learning_logs:index')
