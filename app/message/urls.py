from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_list, name='list'),
    path('<int:user_id>/', views.message_thread, name='thread')
]
