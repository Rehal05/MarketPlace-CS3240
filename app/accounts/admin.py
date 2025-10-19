from django.contrib import admin
from .models import customUser; 

# Register your models here.

@admin.register(customUser) 
class CustomUserAdmin(admin.ModelAdmin): pass