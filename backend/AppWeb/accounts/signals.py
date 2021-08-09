from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from . import models


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	try:
	    if created:
	        models.Profile.objects.create(user=instance)
	    instance.profile.save()
	except:
		pass
	