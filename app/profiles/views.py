from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.views import _is_admin_user

@login_required
def dashboard(request):
    user = request.user
    context = {
        "username": user.username,
        "signup_date": user.date_joined,
        "profile_image_url": user.profile_pic,
        "is_admin": _is_admin_user(user),
    }
    return render(request, "profiles.html", context)
