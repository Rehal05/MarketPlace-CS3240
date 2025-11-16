# accounts/views.py
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from feedapp.models import Report
from message.models import Message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import SignUpForm


def _is_admin_user(user):
    return user.is_superuser or getattr(user, "user_type", "") == "admin"

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # create user
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend') # auto login
            return redirect("/dashboard/")
    else:
        initial = {}
        if 'social_email' in request.session:
            initial['email'] = request.session['social_email']
            request.session.pop('social_email', None)
        form = SignUpForm(initial=initial)
    return render(request, "signup.html", {"form": form})


@login_required
def admin_user_list(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    users = get_user_model().objects.all().order_by("username") # fetch all users
    return render(request, "admin/user_list.html", {"users": users}) # render template with users

@login_required
def admin_conversations(request, user_id):
    if not _is_admin_user(request.user):
        raise PermissionDenied

    User = get_user_model()
    target_user = get_object_or_404(User, id=user_id)

    # Fetch all messages involving this user (sent or received)
    messages = (
        Message.objects.filter(sender=target_user)
        .select_related("receiver")
        .order_by("-timestamp")
    )

    return render(
        request,
        "admin/admin_conversations.html",
        {
            "target_user": target_user,
            "messages": messages,
        }
    )

@login_required
def admin_reports(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    if request.method == "POST":
        report_id = request.POST.get("report_id")
        action = request.POST.get("action")
        report = get_object_or_404(Report, id=report_id)

        if action == "resolve":
            report.status = "resolved"
            report.save()
            messages.success(request, "Report marked as resolved.")
        elif action == "delist":
            post = report.post
            post.is_active = False   # or listing.status = "delisted"
            post.save()
            messages.success(request, "Listing has been delisted.")
        elif action == "ban_user":
            owner = report.post.owner
            owner.is_active = False
            owner.save()
            messages.success(request, "Listing owner has been banned.")
        return redirect("admin_reports")

    reports = Report.objects.select_related("post", "reported_by").all()
    return render(request, "admin/admin_reports.html", {"reports": reports})


@login_required
def admin_dashboard(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    users = get_user_model().objects.all().order_by("username") # fetch all users
    return render(request, "admin/dashboard.html", {"users": users}) # render template with users

