from django.db import models
from django.conf import settings 

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField(blank=True)  # text content
    # allow attaching an uploaded image
    image = models.ImageField(upload_to='uploads/messages/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # store S3 URL
    # Make messages specific to a Post/listing so conversations are per listing
    post = models.ForeignKey(
        'feedapp.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='messages',
    )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        brief = self.content[:20] if self.content else '[image]'
        if self.post:
            return f'{self.sender} -> {self.receiver} on {self.post}: {brief}'
        return f'{self.sender} -> {self.receiver}: {brief}'

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url
