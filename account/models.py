from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True, max_length=50)
    is_email_verified = models.BooleanField(default=False)
    password1 = models.CharField(max_length=20, default='password')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','is_email_verified']


    def __str__(self):
        return str(self.username)

class Profile(models.Model):
    """User profile to extend the account profile
    Added images so they can be displayed on the blog if users comment.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    street_address1 = models.CharField(blank=True, max_length=100, null=True)
    town_or_city = models.CharField(blank=True, max_length=30)
    county = models.CharField(blank=True, default=00, max_length=30, null=True)
    postcode = models.CharField(blank=True, max_length=30)
    avatar = models.ImageField(blank=True, upload_to='profile_pics/')

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<img src="%s" height="50" width="50">' % self.avatar.url
                )
        return "No image found"


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def update_profile(sender, instance, created, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username