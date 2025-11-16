# feedapp/views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Post
from .forms import OfferForm, PostForm

def feed_view(request):
    posts = Post.objects.all()
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

def filter_posts(request):
    qs = Post.objects.select_related('category', 'author')
    q = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    tags = request.GET.get('tags')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if min_price:
        qs = qs.filter(price_min__gte=min_price)
    if max_price:
        qs = qs.filter(price_max__lte=max_price)
    if category:
        qs = qs.filter(category__slug=category)
    if tags:
        tag_tokens = [t.strip().lower() for t in tags.split(',') if t.strip()]
        qs = [post for post in qs if post.matches_tags(tag_tokens)]
    
    return qs

@login_required
def submit_offer(request, post_id):
    post = get_object_or_404(Post, pk=post_id, allow_offers=True)
    if request.method == 'POST':
        form = OfferForm(post, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.post = post
            offer.buyer = request.user
            offer.status = 'pending'
            offer.save()
            if post.min_offer_price and form.cleaned_data['amount'] < post.min_offer_price:
                offer.reject(auto=True)
                messages.warning(request, 'Offer automatically rejected; below seller minimum.')
            else:
                messages.success(request, 'Offer submitted.')
            # optionally create a message thread/notification here
            return redirect('feed')
    else:
        form = OfferForm(post)
    return render(request, 'offer_modal.html', {'form': form, 'post': post})
