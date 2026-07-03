from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import create_unique_slug

class URL(models.Model):
    """
    Stores the original long URL and its compressed Base62 representation.
    """
    long_url = models.URLField(max_length=2000, help_text="The destination URL.")
    short_code = models.CharField(
        max_length=10, 
        unique=True, 
        blank=True,  # Blank=True allows Django forms/serializers to validate without requiring it manually
        help_text="The unique Base62 short token."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Keeps newest links on top

    def __str__(self):
        return f"{self.short_code} -> {self.long_url[:40]}"


@receiver(pre_save, sender=URL)
def auto_generate_short_code(sender, instance, *args, **kwargs):
    """
    Django Signal: Automatically triggers right before a URL row is written 
    to the database. If no short_code exists, it generates a unique one.
    """
    if not instance.short_code:
        instance.short_code = create_unique_slug(instance)

'''
username = charleseffanga
passworld: effangacharles'''