from django.db import models
from django.conf import settings
from django.db.models import Avg

class Report(models.Model):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="reports",
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_filed",
    )

    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="open",
        choices=[
            ("open", "Open"),
            ("resolved", "Resolved"),
        ],
    )

    def __str__(self):
        who = self.reported_by or "Unknown"
        return f"Report on {self.post} by {who}"


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True
    )
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('delisted', 'Delisted')],
        default='active',
        help_text='Whether this post is visible in the feed or delisted by moderators.',
    )

    available = models.BooleanField(default=True)

    #track who the item was sold to 
    sold_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchases'
    )

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
    
    def mark_unavailable(self):
        """Mark listing as unavailable (instead of deleting)."""
        self.available = False
        self.save()
    
    def mark_sold(self, buyer):
        """Mark listing as sold to a user."""
        self.sold_to = buyer
        self.available = False
        self.save()

class Rating(models.Model):
    """Store individual ratings given between users."""
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings_given'
    )

    rated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name='ratings_received'
    )

    post= models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='ratings',
        null=True,
        blank=True
    )
    score= models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rater', 'rated', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rater} rated {self.rated}({self.score})"
    
    @staticmethod
    def get_user_average(user):
        """Compute average rating for a user"""
        result = Rating.objects.filter(rated=user).aggregate(avg=Avg('score'))
        return round(result['avg'], 1) if result['avg'] else None
