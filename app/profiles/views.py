from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from accounts.forms import ProfileEditForm 

@login_required
def dashboard(request):
    user = request.user
    context = {
        "username": user.username,
        "signup_date": user.date_joined,
        "profile_image_url": user.profile_pic,
    }
    return render(request, "profiles.html", context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "edit_profile.html", {"form": form})