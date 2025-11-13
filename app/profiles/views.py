from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from feedapp.models import Rating

@login_required
def dashboard(request):
    user = request.user
    avg_rating = Rating.get_user_average(user)
    context = {
        "username": user.username,
        "signup_date": user.date_joined,
        "profile_image_url": user.profile_pic,
        "avg_rating": avg_rating
    }
    return render(request, "profiles.html", context)
