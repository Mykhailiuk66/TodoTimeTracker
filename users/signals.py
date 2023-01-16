from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        
        profile = Profile.objects.create(
            user = user,
            name = user.first_name,
            username = user.username,
            email = user.email 
        )
        profile.save()
        

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()
        
        

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
