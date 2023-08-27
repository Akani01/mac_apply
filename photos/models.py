from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Category model
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

#Photos model
class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    website_url = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    playstore_url = models.CharField(max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)
    youtube_url = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
   
    def __str__(self):
        return self.description
