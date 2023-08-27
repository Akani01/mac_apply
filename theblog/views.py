from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import Http404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView, CreateView
from .models import Post, Comment, Notification, UserProfile#notification,
from photos.models import Photo, Category
from broker.models import Broker
from members.forms import ProfilePageForm
from .forms import PostForm, EditForm, CommentForm, PostSearchForm 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
#login required 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
#view defined
from django.views import View
from django.core.mail import send_mail
from django.shortcuts import render
#csrf token for email lock
from django.views.decorators.csrf import csrf_protect
from django.conf import settings 

#Homeview 
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/home.html'
    context_object_name = 'posts'
    ordering = ['-post_date']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(author=self.request.user)
    #recently added 
    def get_recently_added_data(self):
        recently_added_broker = Broker.objects.filter(author=self.request.user).order_by('-upload_date').first()
        recently_added_photo = Photo.objects.filter(author=self.request.user).order_by('-upload_date').first()
        return recently_added_broker, recently_added_photo

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        recently_added_broker, recently_added_photo = self.get_recently_added_data()
        
        if recently_added_broker or recently_added_photo:
            return response
        else:
            raise Http404("You are not authorized to view this page.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recently_added_broker, recently_added_photo = self.get_recently_added_data()
        context['recently_added_broker'] = recently_added_broker
        context['recently_added_photo'] = recently_added_photo
        return context
        
#my external redirect urls

def external_redirect(request, url):
    return redirect(url)

#post list views
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        
        return render(request, 'social/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()
        form = CommentForm()
        
        # Retrieve the UserProfile instance associated with the post's author
        profile = UserProfile.objects.get(user=post.author)
        followers = profile.followers.all()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        categories = Category.objects.filter(user=user)

        context = {
            'categories': categories,
            'post': post,
            'form': form,
            'comments': comments,
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            new_comment = Comment(comment=comment_text, post=post, author=user)
            new_comment.save()
            form = CommentForm()  # Clear the form after saving the comment
        
        # Retrieve the UserProfile instance associated with the post's author
        profile = UserProfile.objects.get(user=post.author)
        followers = profile.followers.all()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        categories = Category.objects.filter(user=user)

        context = {
            'categories': categories,
            'post': post,
            'form': form,
            'comments': comments,
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/post_detail.html', context)
    #---END CATEGORY    
#New comment box for the users
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # Save the comment to the database or perform any other necessary actions

        # Create a dictionary with the comment details
        comment_data = {
            'author': request.user.username,
            'created_on': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment_text,
        }

        # Return the comment details as JSON response
        return JsonResponse(comment_data)

    # Handle non-POST requests, if needed
    return render(request, 'comment_form.html')


#AddLike and Dislike the app
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#add like and dislike
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
#--------End


#user search and List followers
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'social/search.html', context)

# followers
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/followers_list.html', context)
#---------End


#Add comment like and dislike
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#Add comments
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
#---------End


#profile

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user

        form = ProfilePageForm(instance=profile)

        followers = profile.followers.all()
        is_following = False

        if request.user.is_authenticated:
            for follower in followers:
                if follower == request.user:
                    is_following = True
                    break

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'form': form,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }
        return render(request, "registration/profile.html", context)

    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        form = ProfilePageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
        else:
            return render(request, "registration/profile.html", {'form': form})
# End__Profile


#PostNotification
class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)


#follow notification and remove notification
class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')
#--------End

#Post edit class
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#---END edit post


#comment delete view
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#---END comment


#Post delete class
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#----END DELETE post


#Comment Reply to users
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('post-detail', pk=post_pk)
#-----END COMMENT VIEW

# Add post section
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social/add_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        # Retrieve recipient email from the form
        recipient_email = self.request.POST.get('recipient_email')

        # Send email notification
        subject = 'New Post Added'
        message = f'A new post has been added.\n\n{form.cleaned_data["title"]}\n{form.cleaned_data["title_tag"]}\n{form.cleaned_data["author"]}\n\n{form.cleaned_data["body"]}\n\n{form.cleaned_data["Where_to_Apply"]}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [recipient_email])

        return super().form_valid(form)


#add comment section
class AddCommentView(CreateView):
    model = Comment  
    form_class = CommentForm
    template_name = 'social/add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    #fields = ('title', 'body')
    success_url = reverse_lazy('home')

#follower add and delete follower
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

#removefollower()
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

#fields = ('title', 'body')
class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = "update_post.html"
    #fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
#search page


#Post search
#search page
def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.objects.filter(
                title__contains=search_string)[:5]

            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug'))

            return JsonResponse({'search_string': data})

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'social/search-file.html',
                  {'form': form,
                   'q': q,
                   'results': results})

#---END title post search


#Each individual must see a unique carousel page
def carousel_page(request):
    if request.user.is_superuser:
        # Admin user can see all posts
        posts = Post.objects.all()
    else:
        # Individual users can only see their own posts
        posts = Post.objects.filter(user=request.user)
    return render(request, 'carousel_page.html', {'posts': posts})