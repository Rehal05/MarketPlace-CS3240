from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
     path("profile/edit/", views.edit_profile, name="edit_profile"),
]
