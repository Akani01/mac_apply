from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Post, Comment
from django.forms import ClearableFileInput
#choices = Applywhere.objects.all().values_list('name','name')

#choice_list = []

#for item in choices:
   # choice_list.append(item)
 
#book form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')

    
#postform
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('about', 'about_tag', 'author', 'body', 'snippet', 'header_image')

        widgets = {
            'about': forms.TextInput(attrs={'class': 'form-control'}),
            'about_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
             
        } 

#edit form
class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('about', 'author', 'body', 'snippet', 'header_image')

        widgets = {
            'about': forms.TextInput(attrs={'class': 'form-control'}),
            #'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),      
        }


#comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body' )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),             
        }
