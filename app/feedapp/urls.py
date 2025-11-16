from django.urls import path
from .views import feed_view, new_post_view
from . import views

urlpatterns = [
    path('', feed_view, name='feed'),
    path('newpost/', new_post_view, name='newpost'),
    path("post/<int:pk>/report/", views.report_post, name="report_post"),

]
