from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.title

    def price_display(self):
        if self.price_min is not None and self.price_max is not None:
            return f"${self.price_min} – ${self.price_max}"
        if self.price_min is not None:
            return f"from ${self.price_min}"
        if self.price_max is not None:
            return f"up to ${self.price_max}"
        return "Price on request"
