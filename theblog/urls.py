from django.urls import path
from .views import HomeView, PostDetailView,  PostListView, AddPostView, PostEditView, PostDeleteView, CommentDeleteView, AddFollower, RemoveFollower, AddLike, AddDislike, UserSearch, ListFollowers, AddCommentLike, AddCommentView, AddCommentDislike, CommentReplyView, ProfileView, PostNotification, FollowNotification, RemoveNotification, PostListView
from django.views.generic import  ListView
from . import views
from django.conf import settings
from django.conf.urls.static import static
#the external redirect url 
from .views import external_redirect


urlpatterns = [
    #home page and main color view
    path('', HomeView.as_view(), name="home"),
    path('post-list/', PostListView.as_view(), name='post-list'),
    #external redirect url
    path('theblog/post/11/<path:url>/', external_redirect, name='external_redirect'),
    #post home
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    #email
    #New comment section
    path('add_comment/', views.add_comment, name='add_comment'),
    #update and detail post
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    #comments
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    #profile
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    #post_search
    path('search_file/', views.post_search, name='post_search'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    #Notifications
    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
