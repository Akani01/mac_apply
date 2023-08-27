from django import forms
from .models import Post, Comment


#Post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'author', 'body', 'Where_to_Apply', 'header_image', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control', 'value':'' , 'id':'elder', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'Where_to_Apply': forms.Textarea(attrs={'class': 'form-control'}),
             
        } 


#end

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'Where_to_Apply')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            #'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'Where_to_Apply': forms.Textarea(attrs={'class': 'form-control'}),
             
        }

#comment form
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

    class Meta:
        model = Comment
        fields = ['comment']
#search model


#post search

#search model

class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Post.objects.all().order_by('title'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control menudd'})
       


#----end post search