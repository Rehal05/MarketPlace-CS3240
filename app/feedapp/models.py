from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models  # if you plan to store lat/lon
from django.utils import timezone
from app.feedapp import forms

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")  # or use django-taggit
    allow_offers = models.BooleanField(default=True)
    min_offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.title

    def get_image_url(self):
        """Return the image URL, preferring uploaded image over image_url field"""
        if self.image:
            return self.image.url
        return self.image_url

    def price_display(self):
        if self.price_min is not None and self.price_max is not None:
            return f"${self.price_min} – ${self.price_max}"
        if self.price_min is not None:
            return f"from ${self.price_min}"
        if self.price_max is not None:
            return f"up to ${self.price_max}"
        return "Price on request"
    
    def clean(self):
        if self.min_offer_price and self.price_min and self.min_offer_price > self.price_min:
            raise ValidationError("Minimum offer cannot exceed the min listing price.")

    def matches_tags(self, query_tags):
        current = {t.strip().lower() for t in self.tags.split(',') if t.strip()}
        return any(tag in current for tag in query_tags)

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('auto_rejected', 'Auto Rejected'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers_made')
    message = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def accept(self):
        self.status = 'accepted'
        self.save(update_fields=['status', 'updated_at'])

    def reject(self, auto=False):
        self.status = 'auto_rejected' if auto else 'rejected'
        self.save(update_fields=['status', 'updated_at'])
