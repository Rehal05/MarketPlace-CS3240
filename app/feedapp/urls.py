from django.urls import path
from .views import feed_view, new_post_view, my_listings_view, toggle_availability_view, mark_sold_review, rate_user_view

urlpatterns = [
    path('', feed_view, name='feed'),
    path('newpost/', new_post_view, name='newpost'),

    #My Listings 
    path('my-listings/', my_listings_view, name='my_listings'),
    path('my-listings/<int:post_id>/toggle/', toggle_availability_view, name='toggle_availability'),
    path('my-listings/<int:post_id>/sold/<int:buyer_id>/', mark_sold_review, name='mark_sold'),

    #Rating Functionality
    path('rate/<int:user_id>/<int:post_id>/', rate_user_view, name='rate_user'),
]
