from django.db import models
from django.contrib.auth.models import AbstractUser #handles username, email, password

# Create your models here.

#user types
USER_TYPE_CHOICES = (
    ('regular', 'Regular User'),
    ('admin', 'Admin User'),
)
class customUser(AbstractUser):
    user_type = models.CharField(
        max_length= 10, 
        choices = USER_TYPE_CHOICES, 
        default='regular'
    )

    bio = models.TextField(blank=True, null=True) #optional text field for short description
    profile_pic = models.URLField(blank=True, null=True) #URL to profile picture from Google

    def __str__(self):
        return self.username