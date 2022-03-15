from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Settings
from wallet.models import Wallet

@receiver(post_save, sender=get_user_model())
def create_user_related(sender, instance, created, **kwargs):

    if created:
        Wallet.objects.create(user = instance)
        Settings.objects.create(user=instance)


