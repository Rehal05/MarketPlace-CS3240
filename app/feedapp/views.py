# feedapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Report
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

def feed_view(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 9)  # 9 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feed.html', {'page_obj': page_obj})

@login_required
def report_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    # Prevent multiple reports from same user on same post
    existing = Report.objects.filter(post=post, reported_by=request.user, status="open")
    if existing.exists():
        messages.info(request, "You already reported this post.")
        return redirect("feed")

    Report.objects.create(
        post=post,
        reported_by=request.user,
        reason="Reported from feed view."
    )

    messages.success(request, "Thanks! A moderator will review this post.")
    return redirect("feed")

