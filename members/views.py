from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.dates import timezone_today
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from theblog.models import UserProfile, Post
from theblog.forms import PostForm
from django.utils import timezone
#forms model
from django import forms
#model_factory
from django.forms.models import modelformset_factory
#send messages3
from django.contrib import messages
#login required mixim
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
#view defined
from django.views import View
# import q
from django.db.models import Q
#New edit profile page view
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import UserProfile
from .forms import UserProfileForm
#create profiles


class CreateProfilePageView(CreateView):
    model = UserProfile
    form_class = ProfilePageForm
    template_name = "registration/create_user_profile_page.html"
    success_url = reverse_lazy('home')  # Replace 'profile' with the appropriate URL name or path

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#edit profiles
class EditProfilePageView(generic.UpdateView):
    model = UserProfile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = reverse_lazy('home')

#show profiles
#class ShowProfilePageView(DetailView):
    #model = UserProfile
    #template_name = 'registration/user_profile.html'
    
    #def get_context_data(self, *args, **kwargs):
        #users = UserProfile.objects.all()
        #context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        #page_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])

        #context ["page_user"] = page_user 
        #return context

class ShowProfilePageView(DetailView):
    model = UserProfile
    template_name = "registration/user_profile.html.html"
    context_object_name = "show_profile_page"  # Use this name in the template for the object

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)
    

#Password Change view
class PasswordsChangeView(PasswordChangeView):
   form_class = PasswordChangingForm
   #from_class = PasswordChangeForm
   #success_url = reverse_lazy('home')
   success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

#user edit view
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
    

#Edit Profile View
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
#End Profiles

class IndexView(generic.ListView):
    paginate_by = 4
    template_name = 'social/post_detail.html'
    context_object_name = 'all_posts'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        if query:
            posts = Post.objects.filter(
                Q(text__icontains=query.capitalize()) |
                Q(title__icontains=query.capitalizw()) |
                Q(text__icontains=query.lower())|
                Q(title__icontains=query.lower())
            ).distinct()
            return posts
        else:
            return Post.objects.filter(date__Ite=timezone.now()).order_by('-date')

