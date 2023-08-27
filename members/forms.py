from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from theblog.models import UserProfile


#profile page
class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture', 'profile_pic', 'website_url', 'google_url', 'zoom_url', 'playstore_url','facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url', 'qr_name', 'qr_code')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'playstore_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'pinterest_url': forms.TextInput(attrs={'class': 'form-control'}),
            'zoom_url': forms.TextInput(attrs={'class': 'form-control'}),
            'google_url': forms.TextInput(attrs={'class': 'form-control'}),
            'qr_name': forms.TextInput(attrs={'class': 'form-control'}),
           
        }

#editView Profile here
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'picture', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url', 'followers']
#End

#signUp
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2' )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


#edit profile
class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined' )

#password changing 
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password' }))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

