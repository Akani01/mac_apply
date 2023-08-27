from django.shortcuts import render, redirect
from .models import Photo, Category
from theblog.models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages
import os


#gallery
@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

#view phot propfirms
@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

#add photo
@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')  # Get the main image

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None
       
        # Check if the main image is provided before creating the photo instance
        if image:
            photo = Photo.objects.create(
                author=user,  # Set the author to the logged-in user
                category=category,
                description=data['description'],
                image=image,  # Use the main image
                website_url=data.get('website_url', ''),
                whatsapp_number=data.get('whatsapp_number', ''),
                facebook_url=data.get('facebook_url', ''),
                location=data.get('location', ''),
                twitter_url=data.get('twitter_url', ''),
                playstore_url=data.get('playstore_url', ''),
                linkedin_url=data.get('linkedin_url', ''),
                instagram_url=data.get('instagram_url', ''),
                pinterest_url=data.get('pinterest_url', ''),
                youtube_url=data.get('youtube_url', ''),
            )
            
            return redirect('gallery')
        else:
            error_message = "Please upload the main image."
            context = {'categories': categories, 'error_message': error_message}
            return render(request, 'photos/add.html', context)

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
  
#galleryview
def galleryview(request):
	photos = Photo.objects.all()
	context = {'photos': photos}
	template = 'photos/listview.html'	
	return render(request, template, context)

#delete gallery image
def deletePhoto(request, pk):
    photos = Photo.objects.get(id=pk)
    if len(photos.image) > 0:
        os.remove(photos.image.path)
    photos.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('social/post_detail.html')

#category view
def CategoryView(request, category):
    user = request.user
    category_posts = Post.objects.filter(user=user)
    return render(request, 'social/categories.html', { category_posts : category_posts})


