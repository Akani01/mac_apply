from django.contrib import admin
from django.urls import path, include
from apply import views
from django.conf import settings
from django.conf.urls.static import static

#this is for notifications

#Django admin header customization
 
admin.site.site_header ="Developed by Akani Ivin Miyen"
admin.site.site_title = "Welcome to Dashboard"
admin.site.index_tile= "Welcome to this Portal"

urlpatterns = [
    #post
    path('projects/', views.ProjectView.as_view(), name="projects"),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('add_project/', views.AddPostView.as_view(), name='add_project'),
    path('article/edit/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove', views.DeletePostView.as_view(), name='delete_post'),
    #book list
    path('about', views.about, name='about'),
    path('book_list/', views.book_list, name='book_list'),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('class/books/', views.BooklistView.as_view(), name='class_book_list'),
    path('class/book/upload', views.UploadBookView.as_view(), name='class_upload_book'),
    #view unique booklist
    path('my-book-list/', views.MyBooklistView.as_view(), name='my_book_list'),
    #post_search
    #this is for likeview
    path('like/<int:pk>/', views.LikeView, name='like_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)