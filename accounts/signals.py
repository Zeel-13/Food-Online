from .models import *
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("user profile is created")
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
            print("user profile is updated")
        except:
            UserProfile.objects.create(user=instance)
            print("user profile does not existed, so created one")

# post_save.connect(post_save_create_profile_reciever,sender=User)

@receiver(pre_save, sender=User)
def pre_save_create_profile_reciever(sender,instance,**kwargs):
    print(instance.username,"is about to be saved")



    