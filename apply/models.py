from django.db import models
from datetime import datetime, date 
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from ckeditor.fields import RichTextField
# Create your models here.

#books
class Book(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
   
    def __str__(self):
        return self.title 

#the post form
class Post(models.Model):
    about = models.CharField(max_length=200)
    header_image = models.ImageField(null=True, blank=True, upload_to="learn/")
    about_tag = models.CharField(max_length=255, default="project!")
    author = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE, related_name='microsecond')
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    snippet = models.CharField(max_length=255, default='Click Link to write more details...')
    likes = models.ManyToManyField(User, related_name='ablog_posts')
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self): 
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        #return reverse("article-detail", args=(str(self.id)) )
        return reverse('projects')

# comment
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

