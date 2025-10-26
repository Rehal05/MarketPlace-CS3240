from django.contrib import admin

# Register your models here.
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')