# feedapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Report
from .forms import PostForm
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
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()

        # Prevent spam: one open report per user+post
        report, created = Report.objects.get_or_create(
            post=post,
            reported_by=request.user,
            status="open",
            defaults={"reason": reason}
        )

        # If they already reported, maybe update the reason
        if not created and reason:
            report.reason = reason
            report.save()

        messages.success(request, "Thanks, your report has been submitted.")
        return redirect("feed")  # adjust to your feed URL name

    # fallback for GET – just go back
    return redirect("feed")

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
