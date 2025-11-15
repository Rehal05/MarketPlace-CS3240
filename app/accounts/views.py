# accounts/views.py
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied

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
def admin_dashboard(request):
    if not _is_admin_user(request.user): # only admin users can access
        raise PermissionDenied 

    users = get_user_model().objects.all().order_by("username") # fetch all users
    return render(request, "admin/dashboard.html", {"users": users}) # render template with users

from message.models import Message  # noqa: E402 (module import after other code)

@login_required
def moderator_user_messages(request, user_id):
    if not _is_admin_user(request.user):
        raise PermissionDenied

    target_user = get_object_or_404(get_user_model(), id=user_id)
    msgs = Message.objects.filter(sender=target_user).select_related('receiver').order_by('timestamp')

    return render(request, "admin/user_messages.html", {
        "target_user": target_user,
        "messages": msgs,
    })