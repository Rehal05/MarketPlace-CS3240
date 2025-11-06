from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('', views.message_list, name='list'),
    path('preview/', views.message_preview, name='preview'),
    path('<int:user_id>/', views.message_thread, name='thread')
]
