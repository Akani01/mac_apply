from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Broker
from photos.models import Category
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView, CreateView
from django.contrib import messages
import os


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        broker = Broker.objects.filter(category__user=user)
    else:
        broker = Broker.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'broker': broker}
    return render(request, 'brokers/brokergallery.html', context)

#view Brokers
@login_required(login_url='login')
def viewBroker(request, pk):
    broker = Broker.objects.get(id=pk)
    return render(request, 'brokers/broker.html', {'broker': broker})

#add broker
@login_required(login_url='login')
def addBroker(request):
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

        # Check if the main image is provided before creating the Broker instance
        if image:
            broker = Broker.objects.create(
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
            
            return redirect('brokergallery')
        else:
            error_message = "Please upload the main image."
            context = {'categories': categories, 'error_message': error_message}
            return render(request, 'brokers/addbroker.html', context)

    context = {'categories': categories}
    return render(request, 'brokers/addbroker.html', context)


#Gallery view here 
def galleryview(request):
	brokers = Broker.objects.all()
	context = {'brokers': brokers}
	template = 'brokers/brokerview.html'	
	return render(request, template, context)

#delete gallery image
def deleteBroker(request, pk):
    broker = get_object_or_404(Broker, id=pk)
    
    # Delete the image file if it exists
    if broker.image:
        if os.path.exists(broker.image.path):
            os.remove(broker.image.path)
    
    broker.delete()
    messages.success(request, "Broker Deleted Successfully")
    
    return redirect('brokergallery')  # Redirect to the appropriate URL pattern


