from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_min', 'price_max', 'created_at')
    search_fields = ('title', 'description')
