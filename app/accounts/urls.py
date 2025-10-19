from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_view, name="signup"), 
    path("moderator/users/", views.admin_user_list, name="user_list"),
    path("moderator/dashboard/", views.admin_dashboard, name = "dashboard"),
]
