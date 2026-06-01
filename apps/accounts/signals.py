from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()


@receiver(pre_delete, sender=User)
def protect_last_superuser(sender, instance, **kwargs):
    if instance.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
        from django.core.exceptions import ValidationError

        raise ValidationError(_("Нельзя удалить единственного superuser."))
