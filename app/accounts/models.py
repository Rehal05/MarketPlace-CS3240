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

    nickname = models.CharField(max_length=50, blank=True, null=True) # Adding nickname in the model
    bio = models.TextField(blank=True, null=True) #optional text field for short description
    profile_pic = models.URLField(blank=True, null=True) #URL to profile picture from Google

    venmo_handle = models.CharField(max_length=64, blank=True, null=True) # e.g. "bill123"
    paypal_handle = models.CharField(max_length=64, blank=True, null=True) # e.g. "bill123" or email
    other_payment_note = models.CharField(max_length=128, blank=True, null=True)
    
    @property
    def venmo_url(self):
        """Build Venmo URL from handle."""
        if self.venmo_handle:
            return f"https://venmo.com/{self.venmo_handle}"
        return None

    @property
    def paypal_url(self):
        """Build PayPal URL from handle."""
        if self.paypal_handle:
            return f"https://www.paypal.me/{self.paypal_handle}"
            # return f"mailto:{self.paypal_handle}"
        return None
    
    def __str__(self):
        return self.username