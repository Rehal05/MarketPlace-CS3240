from django.urls import path
from app.accounts import views
from .views import feed_view, new_post_view

urlpatterns = [
    path('', feed_view, name='feed'),
    path('newpost/', new_post_view, name='newpost'),
    path('posts/<int:post_id>/offer/', views.submit_offer, name='submit-offer'),
]
