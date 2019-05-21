from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from webmain.models import Profile #We need to use model profile added


#WE WANT THESE SIGNALS IN ORDER TO CREATE AND SAVE A NEW PROFILE FOR ALL USERS
@receiver(post_save, sender=User)   #takes as parameter the signal we want and the sender
def create_profile(sender, instance, created, **kwargs):    #takes as parameter instance and created. It means that every time we create a profile
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)       #takes as parameter the signal we want and the sender, We send post_save
def save_profile(sender, instance, **kwargs):
    instance.profile.save()