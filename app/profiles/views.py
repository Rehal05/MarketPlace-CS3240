from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    user = request.user
    context = {
        "username": user.username,
        "signup_date": user.date_joined,
        "profile_image_url": user.profile_pic,
    }
    return render(request, "profiles.html", context)
