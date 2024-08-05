from .models import Profile, Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        author = request.user.profile
        Post.objects.create(author=author, content=content)
        return redirect('home')
    return render(request, 'core/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_profile = request.user.profile
    if user_profile in post.likes.all():
        post.likes.remove(user_profile)
    else:
        post.likes.add(user_profile)
    return redirect('home')

@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        author = request.user.profile
        Comment.objects.create(post=post, author=author, content=content)
        return redirect('home')
    return render(request, 'core/comment.html', {'post': post})

@login_required
def follow_unfollow_user(request, user_id):
    target_profile = get_object_or_404(Profile, user__id=user_id)
    user_profile = request.user.profile
    if target_profile in user_profile.following.all():
        user_profile.following.remove(target_profile)
    else:
        user_profile.following.add(target_profile)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})