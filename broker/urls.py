from django.views.generic import ListView
from .views import galleryview, addBroker, gallery, viewBroker, deleteBroker
from . import views
from django.urls import path
#GalleryView

urlpatterns = [
    path('', views.gallery, name='brokergallery'),
    path('broker/<str:pk>/', views.viewBroker, name='broker'),
    path('addbroker/', views.addBroker, name='addbroker'),
    path('brokerview/', views.galleryview, name='brokerview'),
    path('delete-broker/<str:pk>', views.deleteBroker, name="delete-broker"),
  
]