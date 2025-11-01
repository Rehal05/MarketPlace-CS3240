# feedapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post

def feed_view(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 9)  # 9 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feed.html', {'page_obj': page_obj})
