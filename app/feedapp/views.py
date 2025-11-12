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

#My Listings Page 
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

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        if not post.available:
            messages.error(request, "Cannot edit a sold/unavailable post.")
        
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('my_listings')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})


#Rating Functionality
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min':1, 'max':10, 'step':0.1}),
        }

@login_required
def rate_user_view(request, user_id, post_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    rated_user = get_object_or_404(User, id=user_id)
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                rater = request.user, rated=rated_user, post=post,
                defaults={'score': form.cleaned_data['score']}
            )
            messages.success(request, f"You rated {rated_user.username} {rating.score}/10.")
            return redirect('my_listings')
    else:
        form = RatingForm()
    return render(request, 'rate_user.html', {'form': form, 'rated_user': rated_user})