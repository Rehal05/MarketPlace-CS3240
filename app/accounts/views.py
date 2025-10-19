_# accounts/views.py
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from .forms import SignUpForm


def _is_admin_user(user):
    return user.is_superuser or getattr(user, "user_type", "") == "admin"

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # create user
            login(request, user) # auto login
            return redirect("/dashboard/")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
def admin_user_list(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    users = get_user_model().objects.all().order_by("username") # fetch all users
    return render(request, "admin/user_list.html", {"users": users}) # render template with users

@login_required
def admin_dashboard(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    users = get_user_model().objects.all().order_by("username") # fetch all users
    return render(request, "admin/dashboard.html", {"users": users}) # render template with users

