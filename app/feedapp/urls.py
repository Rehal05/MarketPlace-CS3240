from django.urls import path
from .views import feed_view, new_post_view

urlpatterns = [
    path('', feed_view, name='feed'),
    path('newpost/', new_post_view, name='newpost'),
]
