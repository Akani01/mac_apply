from django.urls import path
from landing.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('landing/index', Index.as_view(), name='index'),
]
