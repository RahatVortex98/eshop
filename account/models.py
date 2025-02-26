from django.db import models  # Import Django's model system
from django.contrib.auth.models import User  # Import built-in User model
from django.db.models.signals import post_save  # Signal that runs after saving a model instance
from django.dispatch import receiver  # Decorator to connect the signal

class Profile(models.Model):
    """
    Extends the built-in User model with additional fields for password reset functionality.
    """
    user = models.OneToOneField(
        User,  # Links this Profile model to a User
        related_name='profile',  # Allows accessing profile as user.profile
        on_delete=models.CASCADE  # Deletes profile when the associated user is deleted
    )
    reset_password_token = models.CharField(
        max_length=50,  # Maximum length of token string
        default="",  # Default value is an empty string
        blank=True  # Field is optional
    )
    reset_password_expire = models.DateTimeField(
        null=True,  # Allows NULL values
        blank=True  # Field is optional
    )

@receiver(post_save, sender=User)  # Runs after a User is saved
def save_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile instance whenever a new User is created.
    """
    user = instance  # Get the saved User instance

    if created:  # Only run when a new user is created (not updated)
        profile = Profile(user=user)  # Create a new Profile for the user
        profile.save()  # Save the Profile in the database
