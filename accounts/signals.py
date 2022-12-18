from django.db.models.signals import post_save

from django.contrib.auth.models import User as DjangoUser

from django.dispatch import receiver
from accounts.models import User


@receiver(post_save, sender=DjangoUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(system_user=instance)


@receiver(post_save, sender=DjangoUser)
def save_profile(sender, instance, **kwargs):
    user = User.objects.get(system_user=instance)
    user.save()
