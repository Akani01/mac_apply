from django.forms.forms import Form
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from datetime import datetime, date 
from django.db.models import Q
from .forms import BookForm, PostForm, EditForm, CommentForm
from .models import Book, Post, Comment
from broker.models import UserProfile
from theblog.models import Notification
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
#login required 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
#view defined
from django.views import View
#start models


 #about   
def about(request):
    #return HttpResponse("This is my about (/about)")
    return render(request, 'about.html')

#projects
def projects(request):
   # return HttpResponse("This is my projects (/projects)")
   return render(request, 'projects.html')

# the book list
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books

    })

def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
            'form': form   
    })

#Booklistview for unique users individuals (code not working right now)
class MyBooklistView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'my_book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        # Filter books by the currently logged-in user
        return Book.objects.filter(user=self.request.user)
#End

#book list view for the domain access
class BooklistView(ListView):  
    model = Book 
    template_name = 'book_list.html'
    context_object_name = 'books'

#upload book
class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'

#home post view
class ProjectView(ListView):
    model = Post
    template_name = 'apply/projects.html'
    ordering = ['-post_date']
    #ordering = ['-id']
    
#post view
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        # profile and followers
        profile = UserProfile.objects.get(pk=pk)
      

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'profile': profile,
       
        }

        return render(request, 'apply/article_detail.html', context)

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


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'apply/article_details.html'

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        # UserProfile
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

#Like button 
def LikeView(request, pk):
    post =  get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

#add post
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'apply/add_project.html'
    #fields = '__all__'
    #fields = ('title', 'body')

#update post
class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = "apply/update_post.html"
    #fields = ['title', 'title_tag', 'body']

#delete post
class DeletePostView(DeleteView):
    model = Post
    template_name = 'apply/delete_post.html'
    success_url = reverse_lazy('home')


#comment form
class AddCommentView(CreateView):
    model = Comment  
    form_class = CommentForm
    template_name = 'apply/add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

