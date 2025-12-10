from django.urls import path
from . import views
from feedapp import views as feedapp_views

app_name = 'message'

urlpatterns = [
    path('', views.message_list, name='list'),
    path('preview/', views.message_preview, name='preview'),
    path('unread/', views.unread_messages, name='unread'),
    path('<int:user_id>/', views.message_thread, name='thread'),
    path('<int:user_id>/<int:post_id>/', views.message_thread, name='thread_with_post'),
    # actions for posts from the thread view
    path('<int:user_id>/<int:post_id>/status/', views.post_status, name='post_status'),
    path('api/unread-count/', views.unread_count_api, name='unread_count_api'),
    path("undo-sale/<int:post_id>/", feedapp_views.undo_sale_view, name="undo_sale"),
]
