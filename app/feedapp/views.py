# feedapp/views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from .models import Post, Rating
from .forms import PostForm
from django import forms

def feed_view(request):
    posts = Post.objects.filter(available=True) #only show available listings
    paginator = Paginator(posts, 9)  # 9 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feed.html', {'page_obj': page_obj})

@login_required
def new_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('dashboard')
    else:
        form = PostForm()
    
    return render(request, 'newpost.html', {'form': form})

@login_required
def my_listings_view(request):
    my_posts = Post.objects.filter(author=request.user)
    return render(request, 'my_listings.html', {'posts': my_posts})

@login_required
def toggle_availability_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.available = not post.available
    post.save()
    messages.success(request, f"Listing marked as { 'available' if post.available else 'unavailable'}.")

@login_required
def mark_sold_review(request, post_id, buyer_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    buyer = get_object_or_404(User, id=buyer_id)
    post.mark_sold(buyer)
    messages.success(request, f"Marked as sold to {buyer.username}.")
    return redirect('my_listings')
